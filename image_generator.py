
# persona_infographic.py
import time
from pydantic import ValidationError
import os
from dotenv import load_dotenv
import argparse
from typing import List
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
load_dotenv()
# ------------------------
# 1. Define the Pydantic Persona Model
# ------------------------
class RedditPersona(BaseModel):
    name: str
    age: int
    occupation: str
    status: str
    location: str
    tier: str
    archetype: str

    summary_quote: str

    motivations: dict  # e.g. {"Convenience": 0.9, ...}
    personality: dict  # e.g. {"Introvert": 0.2, "Extrovert": 0.8, ...}

    behaviour: List[str]
    frustrations: List[str]
    goals: List[str]

# ------------------------
# 2. Load Reddit Text
# ------------------------
def load_reddit_text(username: str) -> str:
    path = f"posts-and-comments/{username}_reddit.txt"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ------------------------
# 3. Call LLM & Parse to Pydantic
# ------------------------
def analyze_persona_structured(reddit_text,max_retries=10,delay=5) -> RedditPersona:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=os.getenv("GOOGLE_API_KEY"),temperature=0.7)
    
    parser = PydanticOutputParser(pydantic_object=RedditPersona)
    fmt = parser.get_format_instructions()

    # Build a single template that includes both placeholders
    system_prompt = """
You are a UX researcher crafting a detailed persona. Extract the following fields as JSON matching our Pydantic schema:
- name, age, occupation, status, location, tier, archetype  
- summary_quote as a short “quote” summarizing their core need  
- motivations: map of motivation names to floats (0-1)  
- personality: map of MBTI dimensions to floats (0-1)  
- behaviour: list of 5 habits  
- frustrations: list of 5 frustrations  
- goals: list of 3 goals  
"""
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "Reddit Content:{reddit_text}")
        ]
        

    )
    
    chain = prompt_template | llm |parser
    for attempt in range(1, max_retries + 1):
        try:
            print(f" Attempt {attempt} to generate persona...")
            return chain.invoke({"reddit_text": reddit_text})
        except ValidationError as e:
            print(f" Validation error (attempt {attempt}): {e}")
        except Exception as e:
            print(f" Other error (attempt {attempt}): {e}")

        time.sleep(delay)

    raise RuntimeError(f"Failed to generate a valid persona after {max_retries} attempts.")

# ------------------------
# 4. Draw Infographic
# ------------------------
def draw_infographic(persona,username):

    from PIL import Image, ImageDraw, ImageFont
    import textwrap

    def load_font(size):
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

    def get_text_size(draw, text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    

    def draw_wrapped_text(draw, text, font, x, y, max_width, line_spacing=4, fill=(0, 0, 0)):
        lines = []
        for paragraph in text.split("\n"):
            avg_char_width = draw.textlength("x", font=font)
            max_chars = max(int(max_width / avg_char_width), 1)
            wrapped = textwrap.wrap(paragraph, width=max_chars)
            lines.extend(wrapped if wrapped else [""])
        draw.multiline_text((x, y), "\n".join(lines), font=font, spacing=line_spacing, fill=fill)
        _, line_height = get_text_size(draw, "Ay", font)
        return line_height * len(lines) + line_spacing * (len(lines) - 1)

    # Font setup
    title_f = load_font(60)
    header_f = load_font(36)
    text_f = load_font(28)
    medium_f = load_font(24)
    # Fixed layout
    W, H = 2200, 1505

    right_col_width = 700
    rx = W - right_col_width - 40
    ry = 50

    tmp_img = Image.new("RGB", (10, 10))
    tmp_draw = ImageDraw.Draw(tmp_img)

    # Right column height estimate
    sections = [persona.behaviour, persona.frustrations, persona.goals]
    right_col_height = 0
    for items in sections:
        right_col_height += 50
        for item in items:
            avg_char_width = tmp_draw.textlength("x", font=text_f)
            max_chars = max(int(right_col_width / avg_char_width), 1)
            wrapped = textwrap.wrap(f"• {item}", width=max_chars)
            right_col_height += len(wrapped) * 34 + 10
        right_col_height += 30

    # Center column height estimate
    center_col_height = 50 + 6 * 40
    center_col_height += 50 + len(persona.motivations) * 70
    center_col_height += 80 + len(persona.personality) * 70

    # Left column height (quote)
    quote_block_height = draw_wrapped_text(tmp_draw, f"“{persona.summary_quote}”", text_f, 0, 0, 460)
    left_col_height = 700 + max(quote_block_height + 40, 300)

    # Create base image with transparency support
    img = Image.new("RGBA", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # --- Left Column rectangle ---
    draw.rectangle((50, 50, 550, 1180), outline="gray", width=2)

    # Load and paste profile image into the left column
    photo = Image.open(f"avatar/{username}.jpg").convert("RGBA")
    photo = photo.resize((500, 1130))
    img.paste(photo, (50, 50), photo)

    # --- Semi-transparent orange overlay (moved up slightly) ---
    qx, qy = 50, 900
    quote_box_height = max(quote_block_height + 30, 300)
    overlay_offset = 25  # how much to move the overlay up
    overlay = Image.new("RGBA", (500, quote_box_height), (230, 81, 0, 180))  # RGBA orange
    img.paste(overlay, (qx, qy - overlay_offset), overlay)

    # --- Quote text (kept slightly lower to stay inside overlay) ---
    draw_wrapped_text(draw, f"“{persona.summary_quote}”", text_f, qx + 20, qy + 20 - overlay_offset, 460, fill="white")

    # --- Center Column ---
    sx, sy = 620, 50
    draw.text((sx, sy), persona.name, font=title_f, fill="#E65100")
    sy += 80

    fields = [
        ("AGE", persona.age),
        ("OCCUPATION", persona.occupation),
        ("STATUS", persona.status),
        ("LOCATION", persona.location),
        ("TIER", persona.tier),
        ("ARCHETYPE", persona.archetype),
    ]

    label_font = medium_f
    value_font = medium_f

    # Define total width allowed for center column (safe limit to avoid third column)
    center_col_max_width = 800  # adjust if needed
    label_width = 200
    value_max_width = center_col_max_width - label_width - 20

    for label, val in fields:
        # Draw the label
        draw.text((sx, sy), f"{label}:", font=label_font, fill="black")

        # Wrap and draw the value within allowed width
        val_x = sx + label_width + 10
        val_y = sy
        avg_char_width = draw.textlength("x", font=value_font)
        max_chars = max(int(value_max_width / avg_char_width), 1)
        wrapped_lines = textwrap.wrap(str(val), width=max_chars)

        for line in wrapped_lines:
            draw.text((val_x, val_y), line, font=value_font, fill="black")
            _, line_h = get_text_size(draw, "Ay", value_font)
            val_y += line_h + 10

        # Move Y downward safely for next field
        sy = max(val_y, sy + line_h + 10)


    # --- Motivations ---
    sy += 60
    motivation_title = "MOTIVATIONS"
    draw.text((sx, sy), motivation_title, font=header_f, fill="#E65100")
    title_w, title_h = get_text_size(draw, motivation_title, header_f)
    line_y = sy + title_h + 12  # 6px below heading
    draw.line((sx, line_y, sx + 700, line_y), fill="gray", width=2)
    sy = line_y + 20  # 10px below line before text

    bar_len = 500
    for key, score in persona.motivations.items():
        draw.text((sx, sy), key, font=text_f, fill="black")
        _, line_h = get_text_size(draw, key, text_f)
        bar_top = sy + line_h + 12
        draw.rectangle((sx + 220, bar_top, sx + 220 + bar_len, bar_top + 20), outline="gray")
        draw.rectangle((sx + 220, bar_top, sx + 220 + int(bar_len * score), bar_top + 20), fill="gray")
        sy = bar_top + 30

    # --- Personality ---
    sy += 60
    personality_title = "PERSONALITY"
    draw.text((sx, sy), personality_title, font=header_f, fill="#E65100")
    title_w, title_h = get_text_size(draw, personality_title, header_f)
    line_y = sy + title_h + 12
    draw.line((sx, line_y, sx + 700, line_y), fill="gray", width=2)
    sy = line_y + 20

    for dim, val in persona.personality.items():
        if " vs " in dim:
            left, right = dim.split(" vs ")
        else:
            left, right = dim, ""
        draw.text((sx, sy), left, font=text_f, fill="black")
        draw.text((sx + 320, sy), right, font=text_f, fill="black")
        slider_y = sy + 30
        draw.rectangle((sx, slider_y, sx + 300, slider_y + 10), outline="gray")
        draw.rectangle((sx, slider_y, sx + int(300 * val), slider_y + 10), fill="gray")
        sy += 70

    # --- Right Column ---
    sections = [
        ("BEHAVIOUR & HABITS", persona.behaviour),
        ("FRUSTRATIONS", persona.frustrations),
        ("GOALS & NEEDS", persona.goals),
    ]
    for title, items in sections:
        draw.text((rx, ry), title, font=header_f, fill="#E65100")
        title_w, title_h = get_text_size(draw, title, header_f)
        line_y = ry + title_h + 12
        draw.line((rx, line_y, rx + right_col_width, line_y), fill="gray", width=2)
        ry = line_y + 20
        for item in items:
            block_h = draw_wrapped_text(draw, f"• {item}", text_f, rx, ry, right_col_width)
            ry += block_h + 15
        ry += 30
    os.makedirs("output", exist_ok=True)
    output_path=f"output/{username}.png"
    img.save(output_path)
    print(f" Persona image saved to: {output_path}")




