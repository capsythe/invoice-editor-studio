# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class InvoiceTemplate(models.Model):
    _name = 'invoice.template'
    _description = 'Invoice Template'
    _order = 'name, id'

    name = fields.Char('Template Name', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    active = fields.Boolean('Active', default=True)
    is_default = fields.Boolean('Default Template', default=False)
    
    # Template Configuration
    template_type = fields.Selection([
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('minimal', 'Minimal'),
        ('professional', 'Professional'),
        ('custom', 'Custom')
    ], string='Template Type', default='modern', required=True)
    
    # Design Settings
    primary_color = fields.Char('Primary Color', default='#667eea', help='Main brand color (hex code)')
    secondary_color = fields.Char('Secondary Color', default='#764ba2', help='Secondary brand color (hex code)')
    text_color = fields.Char('Text Color', default='#333333', help='Main text color (hex code)')
    background_color = fields.Char('Background Color', default='#ffffff', help='Background color (hex code)')
    
    # Typography
    font_family = fields.Selection([
        ('Arial', 'Arial'),
        ('Helvetica', 'Helvetica'),
        ('Times New Roman', 'Times New Roman'),
        ('Georgia', 'Georgia'),
        ('Verdana', 'Verdana'),
        ('Roboto', 'Roboto'),
        ('Open Sans', 'Open Sans'),
    ], string='Font Family', default='Arial')
    
    font_size = fields.Integer('Base Font Size', default=12, help='Base font size in pixels')
    
    # Header Configuration
    show_company_logo = fields.Boolean('Show Company Logo', default=True)
    logo_position = fields.Selection([
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right')
    ], string='Logo Position', default='left')
    
    header_title = fields.Char('Header Title', default='INVOICE', translate=True)
    header_subtitle = fields.Char('Header Subtitle', translate=True)
    show_header_border = fields.Boolean('Show Header Border', default=True)
    
    # Footer Configuration
    footer_text = fields.Html('Footer Text', translate=True, 
                             default='<p>Thank you for your business!</p>')
    show_footer_border = fields.Boolean('Show Footer Border', default=True)
    
    # Table Configuration
    table_style = fields.Selection([
        ('bordered', 'Bordered'),
        ('striped', 'Striped'),
        ('minimal', 'Minimal'),
        ('modern', 'Modern')
    ], string='Table Style', default='modern')
    
    show_table_headers = fields.Boolean('Show Table Headers', default=True)
    table_header_color = fields.Char('Table Header Color', default='#f8f9fa')
    
    # Layout Configuration
    layout_structure = fields.Text('Layout Structure', help='JSON structure of the template layout')
    custom_css = fields.Text('Custom CSS', help='Additional custom CSS styles')
    
    @api.constrains('is_default', 'company_id')
    def _check_default_template(self):
        """Ensure only one default template per company"""
        for record in self:
            if record.is_default:
                existing_default = self.search([
                    ('is_default', '=', True),
                    ('company_id', '=', record.company_id.id),
                    ('id', '!=', record.id)
                ])
                if existing_default:
                    raise ValidationError(_('Only one default template is allowed per company.'))
    
    @api.model
    def get_default_template(self, company_id=None):
        """Get the default template for a company"""
        if not company_id:
            company_id = self.env.company.id
        
        default_template = self.search([
            ('is_default', '=', True),
            ('company_id', '=', company_id),
            ('active', '=', True)
        ], limit=1)
        
        if not default_template:
            # Create a default template if none exists
            default_template = self.create({
                'name': 'Default Invoice Template',
                'description': 'Default invoice template for the company',
                'company_id': company_id,
                'is_default': True,
                'template_type': 'modern',
            })
        
        return default_template
    
    def generate_template_css(self):
        """Generate CSS based on template configuration"""
        css_rules = []
        
        # Base styles
        css_rules.append(f"""
        .invoice-template {{
            font-family: {self.font_family};
            font-size: {self.font_size}px;
            color: {self.text_color};
            background-color: {self.background_color};
        }}
        """)
        
        # Header styles
        css_rules.append(f"""
        .invoice-header {{
            color: {self.primary_color};
            text-align: {self.logo_position};
            {'border-bottom: 2px solid ' + self.primary_color + ';' if self.show_header_border else ''}
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        """)
        
        # Table styles
        table_css = {
            'bordered': f'border: 1px solid {self.primary_color};',
            'striped': 'border-collapse: collapse;',
            'minimal': 'border: none;',
            'modern': f'border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden;'
        }
        
        css_rules.append(f"""
        .invoice-table {{
            {table_css.get(self.table_style, '')}
            width: 100%;
        }}
        
        .invoice-table thead {{
            background: linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%);
            color: white;
        }}
        """)
        
        # Footer styles
        css_rules.append(f"""
        .invoice-footer {{
            {'border-top: 2px solid ' + self.primary_color + ';' if self.show_footer_border else ''}
            padding-top: 20px;
            margin-top: 30px;
            text-align: center;
        }}
        """)
        
        # Add custom CSS
        if self.custom_css:
            css_rules.append(self.custom_css)
        
        return '\n'.join(css_rules)
    
    def preview_template(self):
        """Generate a preview of the template"""
        return {
            'type': 'ir.actions.act_url',
            'url': f'/invoice_studio/preview/{self.id}',
            'target': 'new',
        }
    
    def duplicate_template(self):
        """Create a copy of the template"""
        copy_vals = {
            'name': f"{self.name} (Copy)",
            'is_default': False,
        }
        new_template = self.copy(copy_vals)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.template',
            'res_id': new_template.id,
            'view_mode': 'form',
            'target': 'current',
        }
