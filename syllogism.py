class Syllogism:
    def __init__(self, major_premise, minor_premise, conclusion):
        self.major_premise = major_premise
        self.minor_premise = minor_premise
        self.conclusion = conclusion

    def __repr__(self):
        return f"Major Premise: {self.major_premise}, Minor Premise: {self.minor_premise}, Conclusion: {self.conclusion}"