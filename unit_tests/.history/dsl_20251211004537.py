
class StepParser:
    """Quizizz BDD step parser"""
    def __init__(self):
        self.keywords = ["Given", "When", "Then", "And", "But"]
    
    def parse(self, text):
        if not isinstance(text, str):
            raise TypeError("Step must be a string")
        if not text.strip():
            raise ValueError("Step cannot be empty")
        return text.split()
    
    def validate_step(self, step):
        if not step:
            return False
        words = step.split()
        return words[0] in self.keywords if words else False
    
    def extract_keyword(self, step):
        words = step.split()
        if words and words[0] in self.keywords:
            return words[0]
        return None
    
    def parse_parameters(self, step):
        import re
        params = re.findall(r"'([^']*)'", step)
        return params

class StepRunner:
    """Quizizz BDD step runner"""
    def __init__(self):
        self.executed_steps = []
        self.failed_steps = []
        self.execution_count = 0
    
    def run(self, steps):
        if not isinstance(steps, list):
            raise TypeError("Steps must be a list")
        self.executed_steps.extend(steps)
        self.execution_count += len(steps)
        return [f"EXECUTED: {s}" for s in steps]
    
    def get_executed_steps(self):
        return list(self.executed_steps)
    
    def get_failed_steps(self):
        return list(self.failed_steps)
    
    def reset(self):
        self.executed_steps = []
        self.failed_steps = []
        self.execution_count = 0
    
    def mark_failed(self, step):
        if step not in self.executed_steps:
            raise ValueError("Step was not executed")
        self.failed_steps.append(step)
    
    def get_execution_count(self):
        return self.execution_count


class ScenarioRunner(StepRunner):
    """Legacy alias for StepRunner"""
    pass


class FeatureParser:
    """Quizizz feature file parser"""
    def __init__(self):
        self.features = []
    
    def parse_feature(self, text):
        if not isinstance(text, str):
            raise TypeError("Feature must be a string")
        if not text.strip():
            raise ValueError("Feature cannot be empty")
        self.features.append(text)
        return text.strip()
    
    def get_feature_count(self):
        return len(self.features)
        if step not in self.executed_steps:
            raise ValueError("Step was not executed")
        self.failed_steps.append(step)
    
    def get_execution_count(self):
        return len(self.executed_steps)

class FeatureParser:
    def __init__(self):
        self.features = []
    
    def parse_feature(self, feature_text):
        if not isinstance(feature_text, str):
            raise TypeError("Feature must be a string")
        if not feature_text.strip():
            raise ValueError("Feature cannot be empty")
        self.features.append(feature_text)
        return feature_text.strip()
    
    def get_feature_count(self):
        return len(self.features)
