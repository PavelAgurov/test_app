"""
    List of prompt templates
"""

# pylint: disable=C0301

CLASSIFICATION_PROMPT_TEMPLATE = """
Your task is to classify the given text into one of the following topics.
Topic is not relevant ONLY if topic has property that DIRECTLY contradicts the text.

For example, if text is about "cars" and topic is "animals", then topic is not relevant.
If text is about "cars" and topic is "vehicles", then topic is relevant.
If text is about "cars" and topic is "electric cars", then topic is relevant.

<topics>
{topics}
</topics>

<text>
{text}
</text>
"""

DESCRIPTION_PROMPT_TEMPLATE = """
Your task is to describe item provied by user.
It will be used for similarity search.
Use your knowledge to provide the most accurate description.

Provide answer ONLY in English.
Use simple English and avoid complex sentences.
Do not add too much details, only the most significant ones.

<item>
{item}
</item>
"""

QUESTION_PROMPT_TEMPLATE = """
You are an expert in cargo transportation.
I have a description of DHL-item and list of possible topics from harmonized system.
Your task is to formulate a question that can help to classify the item into one of the topics.
You can ask about properties, features, usage, etc. to make a decision what topic is the most suitable.
Try to cover as much significant information as possible.

Use simple English and avoid complex sentences.
Always answer in English.

Do NOT ask questions that is not required to classify the item.
Do NOT ask questions if you HAVE information from the provided description.

Example1. 
Description: "car".
Topics "passenger car" and "truck, 10-tons".
You should ask ONLY about type of vehicle - "Is it a passenger car or a truck?"

Example2. 
Description: "car".
Topics "passenger car", "truck, less than 10-tons" and "truck, more than 10-tons".
You should ask about type of vehicle and weight - "Is it a passenger car or a truck? What is the weight of the vehicle?"

Example2. 
Description: "car, 2000 kg".
Topics "passenger car", "truck, less than 10-tons" and "truck, more than 10-tons".
You should ask ONLY about type of vehicle - "Is it a passenger car or a truck?"


<topics>
{topics}
</topics>

<description>
{description}
</description>
"""

BUILD_PROPOSED_DESCRIPTION_PROMPT_TEMPLATE = """
You are an expert in cargo transportation.
You have a description of DHL-item and topic from harmonized system.
Your task is to build a good description of the item in scope of the topic.

** Rules:
- Description should be short and contain only the most significant information. 
- Copy ALL properties from the provided description to the answer.
- Do not add too much details, only the most significant ones.
- Use simple English and avoid complex sentences.
- Provide answer ONLY in English.
- Ignore heading references in topics.

** Examples:

Description: "car".
Topic: "passenger car, less than 10 tons".
Answer: "Passenger car, less than 10 tons." (Extend description with topic)

Description: "car, 2000 kg".
Topic: "passenger car, less than 10 tons".
Answer: "Passenger car, 2000 kg." (Combine description and topic)

Description: "t-shirt, cotton, XL".
Topic: "t-shirt, woman, cotton".
Answer: "T-shirt, cotton, wonan, XL." (Extend description with topic)

Description: "t-shirt, cotton, XL".
Topic: "t-shirt, part for machinery of heading 1234".
Answer: "T-shirt, cotton, XL." (Ignore heading reference)

** Input Data:

<topic>
{topic}
</topic>

<user_description>
{user_description}
</user_description>

"""

BUILD_INVOICE_ITEM_LIST_PROMPT_TEMPLATE = """
You are an expert in cargo transportation.
You have a description of DHL-item provided by user and list of topics from harmonized system (HS-code).
For each provided topic you should create a short invoice item as merge of user description and topic.

** Rules:
- Do not add too much details, only the most significant ones.
- You can provide 2-3 options.
- Provide answer ONLY in English.
- Use simple English and avoid complex sentences.
- Ignore heading references in topics.

** Examples:

Description: "car".
Topics: "passenger car, less than 10 tons".
Answer: "Passenger car." (Ignore weight)

Description: "t-shirt, cotton, XL".
Topic: "t-shirt, part for machinery of heading 1234".
Answer: "T-shirt, cotton, XL." (Ignore heading reference)

** Input Data:
<topic_list>
{topic_list}
</topic_list>

<user_description>
{user_description}
</user_description>

"""
IMPROVE_INVOICE_ITEM_PROMPT_TEMPLATE = """
You are an expert in cargo transportation.
User provides DHL invoice item.
Your task is to improve the description of this invoice item.

** Rules:
- Take into account that item is relevant to topic "{relevant_topic}".
- Use simple English. 
- Do not make up information, use only what was provided.
- Ignore heading references in topics.

** Input Data:

<user_description>
{user_description}
</user_description>
"""


GENERATE_INVOICE_PROPERTIES_PROMPT_TEMPLATE = """
You are an expert in cargo transportation. 
I will provide you item description from invoice. 
Please return list of main properties that is required to describe goods but missing in provided description.

Do not include into output:
- Description
- Quantity
- Cost and all properties related to cost
- HS-code
- Dimensions
- Destination and origin

<user_description>
{user_description}
</user_description>
"""