class Module:
    def __init__(
        self,
        subject_code,
        description,
        offering_type,
        half_period,
        full_period,
        final_mark,
        result,
        withheld_reasons,
    ):
        self.subject_code = subject_code
        self.description = description
        self.offering_type = offering_type
        self.half_period = half_period
        self.full_period = full_period
        self.final_mark = final_mark
        self.result = result
        self.withheld_reasons = withheld_reasons

    def to_dict(self):
        return {
            "subject_code": self.subject_code,
            "offering_type": self.offering_type,
            "description": self.description,
            "half_period": self.half_period,
            "full_period": self.full_period,
            "final_mark": self.final_mark,
            "result": self.result,
            "withheld_reasons": self.withheld_reasons,
        }