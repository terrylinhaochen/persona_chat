DIALOGUE_RULES = {
    "Response Structure": {
        "Length": "2-3 sentences maximum per turn",
        "Components": {
            "Quick_Reaction": "1 sentence of immediate response/disagreement",
            "Main_Point": "1-2 sentence with specific example/evidence",
            "Challenge": "End with direct challenge or pointed question"
        }
    },

    "Conflict Generation": {
        "Philosophical Tensions": [
            "Engineering vs Design",
            "Data/AI vs Human Curation",
            "Closed vs Open Systems",
            "Western vs Eastern Market Approaches"
        ],
        "Required Elements": {
            "Direct_Challenge": "Must explicitly disagree with specific point",
            "Counter_Example": "Use real product/market example to counter previous speaker",
            "Technical_Correction": "Interrupt to correct technical inaccuracies",
            "Pointed_Question": "End with challenging question about weak points"
        }
    },
    
    "Depth Requirements": {
        "Technical Detail": {
            "Specs": "Include specific numbers (processing power, latency, costs)",
            "Constraints": "Name explicit technical limitations",
            "Timeline": "Provide concrete development/market timelines"
        },
        "Real World Examples": {
            "Success_Case": "Reference specific successful product/feature",
            "Failure_Case": "Reference specific market/technical failure",
            "Current_Development": "Mention ongoing project/prototype"
        },
        "Metrics": "Use actual market data, user numbers, or technical specifications",
        "Tradeoffs": "Acknowledge specific downsides of proposed approach"
    }
}
