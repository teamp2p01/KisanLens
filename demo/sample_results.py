from ai.schemas import CropAnalysis

DEMO_ANALYSIS = CropAnalysis(
    crop_name="Tomato",
    image_quality="good",
    assessment_status="possible_issue",
    possible_issue="Possible Early Blight",
    confidence=87,
    severity="moderate",
    observed_symptoms=[
        "Dark circular/irregular lesions are visible on the leaves.",
        "Yellowing appears around some affected areas.",
        "The visible pattern is compatible with a fungal leaf-spot problem.",
    ],
    immediate_actions=[
        "Remove severely affected leaves and dispose of plant debris appropriately.",
        "Improve airflow by avoiding overcrowding around the plant.",
        "Avoid repeatedly wetting the foliage when watering.",
    ],
    prevention_steps=[
        "Monitor nearby plants for similar symptoms.",
        "Keep the growing area clean and remove infected plant material.",
        "Maintain appropriate spacing so foliage can dry more quickly.",
    ],
    expert_help_recommended=False,
    expert_help_reason="",
    farmer_summary=(
        "The visible leaf symptoms may be consistent with Early Blight, but a photograph alone "
        "cannot confirm the diagnosis. Start with conservative crop-care steps and monitor whether "
        "the symptoms spread."
    ),
    farmer_summary_hindi=(
        "पत्तियों पर दिख रहे लक्षण अर्ली ब्लाइट जैसी समस्या से मिलते-जुलते हैं, "
        "लेकिन केवल तस्वीर से पक्की बीमारी बताना संभव नहीं है। अभी सावधानी से पौधे की देखभाल करें "
        "और देखें कि लक्षण फैल रहे हैं या नहीं।"
    ),
    immediate_actions_hindi=[
        "बहुत ज्यादा प्रभावित पत्तियों को हटाकर उचित तरीके से नष्ट करें।",
        "पौधों के बीच पर्याप्त दूरी रखें ताकि हवा आसानी से आ-जा सके।",
        "पत्तियों को बार-बार गीला करने के बजाय मिट्टी के पास पानी दें।",
    ],
    prevention_steps_hindi=[
        "आस-पास के पौधों में ऐसे ही लक्षणों पर नजर रखें।",
        "संक्रमित पौधों के अवशेष हटाकर जगह साफ रखें।",
        "पौधों के बीच उचित दूरी बनाए रखें ताकि पत्तियां जल्दी सूख सकें।",
    ],
    demo_mode=True,
)
