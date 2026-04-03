import pytest
from app.services.processor import Processor
from app.models.models import SourceType

def test_normalize_company_name():
    processor = Processor(None)
    assert processor.normalize_company_name("Zepto Inc.") == "Zepto"
    assert processor.normalize_company_name("Flipkart Pvt. Ltd.") == "Flipkart"
    assert processor.normalize_company_name("RELIANCE INDUSTRIES LIMITED") == "Reliance Industries"
    assert processor.normalize_company_name("  Ola Cabs  ") == "Ola Cabs"

def test_extract_company_from_title():
    processor = Processor(None)
    assert processor.extract_company_from_title("Zepto raises $200M in Series E") == "Zepto"
    assert processor.extract_company_from_title("Swiggy appoints new CTO") == "Swiggy"
    assert processor.extract_company_from_title("Unacademy secures funding") == "Unacademy"

def test_score_funding():
    processor = Processor(None)
    assert processor.score_funding("Series A") > 60
    assert processor.score_funding("Seed") < processor.score_funding("Series C")

def test_infer_role_and_dept():
    processor = Processor(None)
    role, dept = processor.infer_role_and_dept("New CTO for Tech")
    assert role == "CTO / VP Engineering"
    assert dept == "Engineering"
