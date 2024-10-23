from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, UUID, Boolean, DateTime

from typing import List
import pyodbc

# Replace the placeholders with your actual server, database, username, and password.
server = '127.0.0.1'
database = 'rulesenginedb'
username = 'sa'
password = 'Becker123'

# Connection string with driver, server, database, username, and password.
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
# engine = pyodbc.connect(conn_str)

SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:Becker123@127.0.0.1:1433/rulesenginedb?driver=ODBC+Driver+17+for+SQL+Server"

Base = declarative_base()


class Workflow(Base):
    __tablename__ = "WORKFLOWS"

    def __init__(self):
        # self.WorkflowRules = set()
        pass

    WorkflowId = Column("WORKFLOW_ID", Integer, primary_key=True)
    Uuid = Column("UUID", UUID)
    Description = Column("DESCRIPTION", String)
    IsActiveFlag = Column("IS_ACTIVE_FLAG", Boolean)
    # WorkflowRules: Mapped[List["WorkflowRule"]] = relationship(back_populates="Workflow")


class AggregateOperator(Base):
    __tablename__ = "AGGREGATE_OPERATORS"

    def __init__(self):
        # self.WorkflowRules = set()
        # self.CriteriaRules = set()
        pass

    AggregateOperatorId = Column("AGGREGATE_OPERATOR_ID", Integer, primary_key=True)
    Uuid = Column("UUID", UUID)
    Operator = Column("OPERATOR",String)


class WorkflowRule(Base):
    __tablename__ = "WORKFLOW_RULES"

    def __init__(self):
        # self.inverse_parent_workflow_rule = set()
        # self.tenant_rules = set()
        # self.tenant_inner_rules = set()
        # self.workflow_rule_criteria_rules = set()
        # self.workflow = None
        # self.aggregate_operator = None
        # self.parent_workflow_rule = None
        pass

    workflow_rule_id = Column("WORKFLOW_RULE_ID", Integer, primary_key=True)
    workflow_id = Column("WORKFLOW_ID", Integer, ForeignKey("FK_WORKFLOW_RULES_WORKFLOWS"))
    description = Column("DESCRIPTION", String)
    rule_json = Column("RULE_JSON",String)
    aggregate_operator_id = Column("AGGREGATE_OPERATOR_ID", Integer)
    parent_workflow_rule_id = Column("PARENT_WORKFLOW_RULE_ID", Integer)
    rule_custom_arguments_count = Column("RULE_CUSTOM_ARGUMENTS_COUNT", Integer)
    workflow_rule_uid = Column("WORKFLOW_RULE_UID", UUID)

    tenant_rules: Mapped[List["TenantRule"]] = relationship(back_populates="WorkflowRule")
    

class CriteriaRule(Base):
    __tablename__ = "CRITERIA_RULES"

    def __init__(self):
        # self.AggregateOperator = None
        # self.ParentCriteriaRule = None
        # self.InverseParentCriteriaRule = set()
        # self.WorkflowRuleCriteriaRules = set()
        pass

    CriteriaRuleId = Column("CRITERIA_RULE_ID", Integer, primary_key=True)
    Description = Column("DESCRIPTION", String)
    RuleJson = Column("RULE_JSON", String)
    AggregateOperatorId = Column("AGGREGATE_OPERATOR_ID", Integer)
    ParentCriteriaRuleId = Column("PARENT_CRITERIA_RULE_ID", Integer)
        

class WorkflowRuleCriteriaRule(Base):
    __tablename__ = "WORKFLOW_RULE_CRITERIA_RULES"

    def __init__(self):
        # self.CriteriaRuleNavigation = None
        # self.WorkflowRuleNavigation = None
        pass

    WorkflowRuleCriteriaRuleId = Column("WORKFLOW_RULE_CRITERIA_RULE_ID", Integer, primary_key=True)
    WorkflowRuleId = Column("WORKFLOW_RULE_ID", Integer)
    CriteriaRuleId = Column("CRITERIA_RULE_ID", Integer)
        

class TenantRule(Base):
    __tablename__ = "TENANT_RULES"

    def __init__(self):
        
        # self.Tenant = None
        # self.WorkflowRule = None
        pass

    TenantRuleId = Column("TENANT_RULE_ID", Integer, primary_key=True)
    TenantId = Column("TENANT_ID", Integer)
    WorkflowRuleId = Column("WORKFLOW_RULE_ID", Integer, ForeignKey("WORKFLOW_RULES.WORKFLOW_RULE_ID"))
    IsActiveFlag = Column("IS_ACTIVE_FLAG", Boolean)
    EffectiveDate = Column("EFFECTIVE_DATE", DateTime)
    TerminationDate = Column("TERMINATION_DATE", DateTime)
    IsGlobalRule = Column("IS_GLOBAL_RULE", Boolean)
    ParentRuleUniqueIdentifier = Column("PARENT_RULE_UNIQUE_IDENTIFIER", UUID)
    RuleUniqueIdentifier = Column("RULE_UNIQUE_IDENTIFIER", UUID)
    RuleCustomArgumentsValue = Column("RULE_CUSTOM_ARGUMENTS_VALUE", String)
    CriteriasCustomArgumentsValue = Column("CRITERIAS_CUSTOM_ARGUMENTS_VALUE", String)

    WorkflowRule: Mapped["WorkflowRule"] = relationship(back_populates="tenant_rules")


class TenantInnerRule(Base):
    __tablename__ = "TENANT_INNER_RULES"

    def __init__(self):
        # self.RuleCustomArgumentsValue = []
        # self.CriteriasCustomArgumentsValue = []
        # self.Tenant = None
        # self.WorkflowRule = None
        pass

    TenantInnerRuleId = Column(Integer, primary_key=True)
    TenantId = Column("TENANT_ID", Integer)
    CustomerId = Column("CUSTOMER_ID", Integer)
    WorkflowRuleId = Column("WORKFLOW_RULE_ID", Integer)
    IsActiveFlag = Column("IS_ACTIVE_FLAG", Boolean)
    EffectiveDate = Column("EFFECTIVE_DATE", DateTime)
    TerminationDate = Column("TERMINATION_DATE", DateTime)
    UserIdLastModified = Column("USER_ID_LAST_MODIFIED", Integer)
    DateLastModified = Column("DATE_LAST_MODIFIED", DateTime)
    RuleUniqueIdentifier = Column("RULE_UNIQUE_IDENTIFIER", UUID)
    GlobalRuleUniqueIdentifier = Column("GLOBAL_RULE_UNIQUE_IDENTIFIER", UUID)
    ParentRuleUniqueIdentifier = Column("PARENT_RULE_UNIQUE_IDENTIFIER", UUID)
    RuleCustomArgumentsValue = Column("RULE_CUSTOM_ARGUMENTS_VALUE", String)
    CriteriasCustomArgumentsValue = Column("CRITERIAS_CUSTOM_ARGUMENTS_VALUE", String)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()