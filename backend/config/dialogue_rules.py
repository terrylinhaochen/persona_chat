DIALOGUE_RULES = {
    "dialogue_flow": {
        "opening_phase": {
            "host": "State specific concern, invite first guest (2 sentences)",
            "guest_first": "Share core experience (2 sentences)"
        },
        "interaction_phase": {
            "host": "Single question, invite next guest",
            "guest_response": "Share specific experience (2 sentences)",
            "interactive_comment": "Resonate with others' experiences (1 sentence)"
        }
    },
    
    "expression_requirements": {
        "must_include": {
            "specific_time": "Year, specific events",
            "real_details": "Historical background, personal experience",
            "emotional_resonance": "Connection with others' experiences"
        },
        "strictly_forbidden": {
            "long_speech": "No more than 2 sentences per turn",
            "vague_preaching": "Must include specific examples",
            "off_topic": "Must address host's stated concern"
        }
    }
}