def detect_keywords(text, keyword_dict):
    matches = []
    for theme, keywords in keyword_dict.items():
        for keyword in keywords:
            if keyword in text:
                matches.append(theme)
                break
    return matches

def get_negative_keywords():
    return {
        "Qualidade Ruim do Produto": [
            "broken", "cheap", "poor", "defective", "fragile", "bad quality", 
            "didn't work", "not working", "flimsy", "scratched", "low quality", 
            "unreliable", "faulty", "malfunctioning", "subpar", "shoddy", "imperfect"
        ],
        "Problemas na Entrega": [
            "late", "delayed", "didn't arrive", "wrong item", "missing", 
            "damaged box", "arrived broken", "not delivered", "shipping issues", 
            "lost package", "arrived after promised date", "wrong delivery address"
        ],
        "Atendimento": [
            "support", "customer service", "no response", "rude", "unhelpful", 
            "ignored", "unfriendly", "unprofessional", "slow response", 
            "unresponsive", "unavailable", "poor service", "dismissive"
        ],
        "Expectativa não Atendida": [
            "not as described", "disappointed", "misleading", "not like picture", 
            "false advertisement", "doesn't match", "underwhelming", "not what I expected", 
            "unfulfilled promises", "unmet expectations", "misrepresentation"
        ],
        "Preço": [
            "expensive", "overpriced", "not worth", "too much", "waste of money", 
            "too costly", "exorbitant", "pricey", "ridiculously expensive", 
            "not a good deal", "price not justified", "overvalued"
        ],
        "Usabilidade do Produto": [
            "hard to use", "complicated", "manual", "instructions unclear", 
            "doesn't fit", "incompatible", "difficult to assemble", "hard to set up", 
            "complex", "confusing", "user-unfriendly", "too technical", 
            "no clear instructions", "awkward to use", "poor design"
        ],
        "Funcionamento Inadequado": [
            "doesn't work", "stops working", "malfunctions", "doesn't function properly", 
            "constantly breaks", "not responsive", "broken after use", "stopped working", 
            "doesn't turn on", "stopped functioning"
        ],
        "Problemas de Durabilidade": [
            "short lifespan", "wears out quickly", "breaks easily", "doesn't last", 
            "broke after a few uses", "poor durability", "wears down", "low durability", 
            "fragile over time", "fades quickly"
        ],
        "Problemas de Desempenho": [
            "slow", "lags", "not fast enough", "underperforming", "low performance", 
            "doesn't meet expectations", "poor speed", "unresponsive", 
            "doesn't perform as expected", "sluggish", "not efficient"
        ],
        "Problemas de Design": [
            "ugly", "poor design", "too bulky", "awkward", "unattractive", "clunky", 
            "uncomfortable", "poor aesthetics", "unappealing", "doesn't look good"
        ]
    }

def get_positive_keywords():
    return {
        "Qualidade do Produto": [
            "high quality", "well made", "excellent quality", "durable", "reliable",
            "great build", "solid", "premium", "top-notch", "superior", "flawless",
            "robust", "perfect condition", "sturdy", "works perfectly"
        ],
        "Entrega Eficiente": [
            "on time", "fast delivery", "quick shipping", "arrived early", "prompt delivery",
            "delivered as promised", "received quickly", "ahead of schedule",
            "timely", "no issues with delivery", "well packaged"
        ],
        "Atendimento ao Cliente": [
            "helpful support", "great customer service", "quick response", "friendly staff",
            "responsive", "polite", "professional", "attentive", "solved my problem",
            "supportive", "courteous", "efficient service"
        ],
        "Superou Expectativas": [
            "better than expected", "exceeded expectations", "pleasantly surprised",
            "beyond what I hoped", "impressed", "delighted", "fantastic experience",
            "exceptional", "thrilled", "outstanding", "amazed", "wow factor"
        ],
        "Bom Custo-Benefício": [
            "worth the price", "great value", "good deal", "affordable", "inexpensive",
            "fair price", "reasonable cost", "economical", "budget-friendly",
            "cost-effective", "excellent value", "money well spent"
        ],
        "Fácil de Usar": [
            "easy to use", "user-friendly", "intuitive", "simple setup", "clear instructions",
            "straightforward", "easy to assemble", "plug and play", "no hassle",
            "convenient", "works out of the box"
        ],
        "Bom Funcionamento": [
            "works great", "functions perfectly", "no problems", "runs smoothly",
            "performs well", "flawless operation", "stable performance", "does the job",
            "reliable performance", "consistent results"
        ],
        "Alta Durabilidade": [
            "long-lasting", "built to last", "durable", "stays strong", "resilient",
            "withstands use", "holds up well", "still like new", "good longevity",
            "maintains quality over time"
        ],
        "Bom Desempenho": [
            "fast", "efficient", "powerful", "high performance", "snappy", "responsive",
            "impressive speed", "delivers results", "performs like a champ",
            "handles well", "meets all my needs"
        ],
        "Design Agradável": [
            "beautiful", "sleek design", "stylish", "modern look", "elegant", "compact",
            "visually appealing", "great aesthetics", "nice appearance", "well designed",
            "comfortable", "pleasing to the eye"
        ]
    }

def detect_themes(df):
    negative_keywords = get_negative_keywords()
    positive_keywords = get_positive_keywords()
    
    df["themes"] = df["clean_text"].apply(lambda x: detect_keywords(x, negative_keywords))
    df["positive_themes"] = df["clean_text"].apply(lambda x: detect_keywords(x, positive_keywords))
    
    return df