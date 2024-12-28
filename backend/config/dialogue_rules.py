DIALOGUE_RULES = {
    "Response Structure": {
        "Length": "2-3 sentences maximum per turn",
        "Components": {
            "Quick_Reaction": {
                "Style": "Immediate interruption or disagreement",
                "Length": "1 sharp, personality-driven sentence",
                "Examples": {
                    "Musk": "Sorry, but that's physically impossible - let me show you why.",
                    "Jobs": "This is exactly what's wrong with engineer-only thinking.",
                    "Zhang": "The data completely contradicts that assumption."
                }
            },
            "Main_Point": {
                "Length": "1-2 sentences",
                "Must_Include": [
                    "Specific technical/market detail",
                    "Personal experience reference"
                ]
            },
            "Closing": {
                "Style": "Strong stance or correction",
                "Types": {
                    "Musk": ["Technical correction", "Engineering challenge", "Timeline reality check"],
                    "Jobs": ["Design criticism", "Integration imperative", "Experience requirement"],
                    "Zhang": ["Data contradiction", "Market reality", "Scalability issue"]
                }
            }
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
            "Technical_Correction": "Interrupt to correct technical inaccuracies"
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