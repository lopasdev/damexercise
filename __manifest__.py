# -*- coding: utf-8 -*-
{
    'name': "Lopan Market",  # Module title
    'summary': "Manage products easily",  # Module subtitle phrase
    'description': """
Manage Market
==============
Description related to Market.
    """,  # Supports reStructuredText(RST) format
    'proveedor': "Parth Gajjar",
    'website': "http://www.example.com",
    'category': 'Tools',
    'version': '15.0.0',
    'depends': ['base'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'views/library_book_categ.xml',
        'views/partner.xml',
        'reports/books_report.xml',
        # Si no carga demo data, este siempre carga
        #'demo/demo.xml',              
    ],
    # This demo data files will be loaded if db initialize with demo data (commented becaues file is not added in this example)
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,    
}
