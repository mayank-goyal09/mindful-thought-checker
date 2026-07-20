# Database of cognitive distortions with definitions, examples, and reframing strategies.

DISTORTIONS_MAP = {
    0: {
        "name": "Catastrophizing",
        "description": "Anticipating the worst possible outcome, magnifying a minor setback, or assuming disaster will strike no matter what.",
        "examples": [
            "If I fail this exam, I'll drop out of college and my life will be ruined.",
            "My chest feels a bit tight; I must be having a heart attack."
        ],
        "reframing_questions": [
            "What is the actual probability of the worst-case scenario happening?",
            "What is the best-case scenario?",
            "What is the most realistic or likely outcome?",
            "If the worst did happen, how would I cope with it?"
        ],
        "reframing_advice": "De-catastrophize by separating feelings from facts. Break down the situation and identify practical steps you can take to handle the actual likely outcomes."
    },
    1: {
        "name": "Mental Filter",
        "description": "Focusing exclusively on the negative aspects of a situation while completely filtering out or dismissing all positive elements.",
        "examples": [
            "I got a 95% on my presentation, but I made that one typo on slide 4. I'm terrible at public speaking.",
            "My friend didn't reply to my text for three hours. They must hate me."
        ],
        "reframing_questions": [
            "Am I looking at only the negative evidence while ignoring the positives?",
            "If I looked at this situation from an objective outsider's perspective, what would they see?",
            "What positive details or achievements am I leaving out?"
        ],
        "reframing_advice": "Balance the ledger. Make a conscious effort to list at least three positive or neutral aspects of the situation to counter the negative filter."
    },
    2: {
        "name": "Neutral",
        "description": "No cognitive distortion detected. The thought process appears objective, balanced, and grounded in realistic facts.",
        "examples": [
            "I'm feeling stressed about the upcoming deadline, but I'll make a schedule to get it done.",
            "We had an argument, but we'll talk about it tomorrow when we are both calmer."
        ],
        "reframing_questions": [],
        "reframing_advice": "Your thinking is balanced and grounded. Continue observing your thoughts with mindfulness and maintaining this realistic perspective."
    },
    3: {
        "name": "Personalization",
        "description": "Holding yourself personally responsible for events that are not entirely in your control, or assuming others' behaviors are a direct reaction to you.",
        "examples": [
            "Our team lost the project bid. It's entirely my fault because my section wasn't perfect.",
            "My partner is quiet tonight; I must have done something to upset them."
        ],
        "reframing_questions": [
            "What other factors (outside of myself) contributed to this outcome?",
            "Am I taking responsibility for things I cannot control?",
            "Why might the other person be acting this way that has absolutely nothing to do with me?"
        ],
        "reframing_advice": "Draw a 'pie chart of responsibility'. List all the external factors (other people, environment, timing, chance) and assign percentages to show that you are only one small piece of the outcome."
    },
    4: {
        "name": "Should Statements",
        "description": "Holding rigid, unrealistic rules for yourself or others, often using words like 'should', 'must', or 'ought to'. This leads to guilt, anger, and frustration.",
        "examples": [
            "I should never make mistakes at work.",
            "They ought to know that their behavior is bothering me without me telling them."
        ],
        "reframing_questions": [
            "Why must this rule always apply? Is it realistic?",
            "What happens if I replace 'should' or 'must' with 'I would prefer to' or 'It would be nice if'?",
            "Am I demanding perfection from myself or others in an imperfect world?"
        ],
        "reframing_advice": "Reframe rules into preferences. Replace rigid 'should' statements with flexible, compassionate language like 'It would be nice if...' or 'I will do my best to...'."
    }
}
