{
    'name': 'Project Management System',
    'version': '1.1',
    'category': '',
    'summary': 'Project Management',
    'depends': ['base','bus'],
    'data': [
        "security/ir.model.access.csv",
        'data/ir_sequence.xml',
        'views/project_details.xml',
        'views/task_details.xml',
        'data/ir.cron.xml'
    ],
    'application' : True,
}