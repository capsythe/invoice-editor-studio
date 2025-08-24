# -*- coding: utf-8 -*-
{
    'name': 'Invoice Editor Studio - Professional Edition',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Invoicing',
    'summary': 'Professional Visual Invoice Template Editor - Studio-like WYSIWYG interface for creating stunning invoice layouts',
    'description': """
        Invoice Editor Studio - Professional Edition
        ============================================
        
        Transform your invoice design process with our powerful visual editor that rivals Odoo Studio's capabilities.
        Create stunning, professional invoice templates without any coding knowledge.
        
        🎨 Key Features:
        ---------------
        ✅ Visual drag-and-drop invoice template editor
        ✅ Real-time preview with live editing
        ✅ Professional pre-built templates and themes
        ✅ Advanced element positioning and styling
        ✅ Company branding and logo integration
        ✅ Complete color scheme and typography control
        ✅ Dynamic header and footer customization
        ✅ Flexible table layout modifications
        ✅ Template export/import capabilities
        ✅ Multi-company template management
        ✅ Responsive design for all devices
        ✅ Professional support and updates
        
        🚀 Perfect For:
        ---------------
        • Businesses requiring branded, professional invoices
        • Companies with multiple invoice formats
        • Organizations needing consistent branding
        • Users who want Studio-like capabilities for invoices
        • Professional service providers
        
        📞 Support & Licensing:
        ----------------------
        This is a premium, proprietary module developed by Capsythe.
        Professional support, updates, and customization services available.
        
        Contact us for licensing, enterprise features, and custom development.
    """,
    'author': 'Capsythe',
    'website': 'https://capsythe.com',
    'license': 'OPL-1',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/invoice_template_views.xml',
        'views/invoice_studio_menus.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
}
