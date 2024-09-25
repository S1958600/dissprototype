class Syllogism:
    def __init__(self, major_premise, minor_premise, conclusion):
        self.major_premise = major_premise
        self.minor_premise = minor_premise
        self.conclusion = conclusion

    def __str__(self):
        return f"Major Premise: {self.major_premise}\nMinor Premise: {self.minor_premise}\nConclusion: {self.conclusion}"