from flask import Flask
from datetime import datetime
from requests import product, mapperExpression
from requests.product import ProductActions, InvoiceActions
import re
from database.sql_alchemy_sqlserver import session, Workflow, WorkflowRule, TenantRule
import pyodbc
import json

app = Flask(__name__)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4999)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/hello/<name>")
def hello_there(name):
    print(pyodbc.drivers())
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now

    return content

@app.route("/rule_poc")
def rules_testing():
    datatata = session.query(Workflow).all()

    tenant_rules = session.query(TenantRule)

    rule_to_check = ""
    for tr in tenant_rules:
        arguments = json.loads(tr.RuleCustomArgumentsValue)
        rule_json_string = tr.WorkflowRule.rule_json
        for arg in arguments:
            argname = arg["ArgumentName"]
            argvalue = arg["ArgumentValue"]
            print(type(rule_json_string))
            rule_json_string = rule_json_string.replace(argname, argvalue)
        print(tr.TenantId)
        print(tr.WorkflowRule.rule_json)
        print(rule_json_string)
        rule_to_check = rule_json_string

    dic_rule_to_check = json.loads(rule_to_check)

    documents = [product.InvoiceDocument("Delivery Receipt"), product.InvoiceDocument("Bill of Lading")]
    input2 = product.Invoice(documents)
    # input2.Documents = documents
    invoice_actions = InvoiceActions(input2)
    result_expression = f'lambda input : {dic_rule_to_check["Expression"]}'

    rule_expression_string = 'lambda input : all( dm in [ d.DocumentTypeDescription for d in input.Documents ] or dm.strip() == "" for dm in "Bill of Lading,Delivery Receipt".split(",") ) '
    result_boolean1231 = eval(rule_expression_string, globals(), {k: getattr(input2, k) for k in dir(input2)})
    result_Asdasd = result_boolean1231(input2)
    result_boolean = eval(result_expression, globals(), {k: getattr(input2, k) for k in dir(input2)})
    if result_boolean(input2):
        # for act in dic_rule_to_check["Actions"]:
        #     do_actions(dic_rule_to_check["Actions"], invoice_actions)
        do_actions(dic_rule_to_check["Actions"], invoice_actions)

    dfdf = testing(product.Producto())


def testing(product):
    expressionInString = "product.age > product.quantity"
    resul = lambda product : eval(expressionInString)

    actionsFor = ProductActions(product)
    rules123 = [
        {
            "conditions": 
            {
                "all": [
                    {
                        "itemobject1": {
                            "name": "quantity",
                            "typeobject" : "field"
                        },
                        "operator": "less_than",
                        "itemobject2": {
                            "name": "age",
                            "typeobject" : "field"
                        }
                    }
                ]
            }
        }
    ]
    rules = [
{ "conditions": { "all": [
      { "name": "expiration_days",
        "operator": "less_than",
        "value": "expiration_days",
      },
      { "name": "current_inventory",
        "operator": "greater_than",
        "value": 20,
      },
  ]},
  "actions": [
      { "name": "put_on_sale",
        "params": {"sale_percentage": 0.25},
      },
      { "name": "put_on_sale22",
        "params": {"sale_percentage": 0.25},
      },
  ],
}] 
    
    check_conditions(rules123[0]["conditions"], product)
    action = rules[0]["actions"]

    ASDASFA = resul(product)
    if resul(product):
        do_actions(action, actionsFor)

    return resul(product)


def do_actions(actions, defined_actions):
    print(f'este es el tipo de el grupo de actions {type(actions)}')
    for action in actions:
        print(f'este es el tipo de un action {type(action)}')
        method_name = action['name']
        def fallback(*args, **kwargs):
            raise AssertionError("Action {0} is not defined in class {1}"\
                    .format(method_name, defined_actions.__class__.__name__))
        params = action.get('params') or {}
        method = getattr(defined_actions, method_name, fallback)
        method(**params)

def check_conditions(conditions, subject):
    mapperExpression.check_conditions_recursively(conditions, subject)




# class Invoice:
#     Documents = []

#     def __init__(self):
#         self.Documents = [InvoiceDocument("asdasda")]


# class InvoiceDocument:
#     DocumentTypeDescription = None

#     def __init__(self, DocumentTypeDescription):
#         self.DocumentTypeDescription = DocumentTypeDescription

