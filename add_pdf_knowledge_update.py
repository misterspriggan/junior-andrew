from pathlib import Path
import shutil
from datetime import datetime

BASE = Path(r"C:\AI-Mailbox-Analysis\junior_andrew_deploy")
KNOWLEDGE = BASE / "knowledge"
BACKUP_ROOT = Path(r"C:\AI-Mailbox-Analysis\backup")
APP_FILE = BASE / "junior_andrew_web_app.py"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = BACKUP_ROOT / f"junior_andrew_before_pdf_knowledge_{timestamp}"

backup_dir.mkdir(parents=True, exist_ok=True)
(backup_dir / "knowledge").mkdir(parents=True, exist_ok=True)

for file_name in ["junior_andrew_web_app.py", "requirements.txt"]:
    src = BASE / file_name
    if src.exists():
        shutil.copy2(src, backup_dir / file_name)

for src in KNOWLEDGE.glob("*.txt"):
    shutil.copy2(src, backup_dir / "knowledge" / src.name)

files = {
    "build_instruction_guardrails.txt": r"""
BUILD INSTRUCTION GUARDRAILS

This file teaches Junior Andrew how to handle build-instruction questions safely.

GENERAL RULE

Patio cover build instruction PDFs are general installation instruction packets.

They are not specific to the customer’s exact design.

Every customer’s quote, final design, parts checklist, attachment method, post layout, footing depth, post inserts, header inserts, engineering, region, and selected options can change the build details.

Junior Andrew can explain general build concepts, but should not replace the customer’s quote, final design, parts checklist, representative, engineering packet, or build support.

If a customer has already ordered, build support can pull up the customer’s specific design and give much better project-specific guidance.

BUILD SUPPORT HANDOFF

If the customer asks a specific install question, Junior Andrew should usually say something like:

“I can give you the general idea, but your exact quote, final design, and parts checklist matter here. If you’ve already ordered, build support can pull up your specific design and give much better guidance.”

If useful, provide the company number:

(888) 851-8351

Use this especially for questions about:

- exact post locations
- footing depth
- steel post inserts
- post footprint
- attachment type
- hanger placement
- header beam inserts
- steel C-beams
- rafter spacing
- roof panel cutting
- trim lengths
- fastener selection
- region-specific instructions
- permit or engineering requirements
- anything the customer is physically cutting, anchoring, or installing

CUSTOM / REGION-SPECIFIC WARNING

Some instruction files may be location-specific or region-specific.

If a document says East, West, Central, Texas, or refers to manufacturer differences, do not assume those details apply everywhere.

Say:

“Some instructions can vary by region or manufacturer, so I’d treat that as general guidance and confirm the exact version for your project.”

GENERAL BUILD-PACKET THEMES

The instruction packets commonly emphasize:

- review the quote that was emailed by the sales representative
- the quote dictates measurements, post footprint, and footing depth if applicable
- the instructions are general and not specific to every design
- homes are not perfectly square
- some on-site trimming is expected
- hanger channel, gutter, front fascia, side fascia, and posts may need trimming on most non-insulated or insulated kits
- lattice kits are generally manufactured to exact lengths, but material should still be measured to confirm
- some kits may include steel or aluminum post inserts
- some kits may include steel C-beam inserts inside 3x8 header beams
- every kit varies in design and application
- measure twice and cut once

STEEL INSERT CAUTION

If a customer asks about steel post inserts:

Some steel post inserts may not allow the post sleeve to slide over the insert normally.

In those cases, the instructions may require scoring the seam of the post sleeve/wrap and wrapping it around the insert.

This does not apply the same way to steel clover or aluminum clover inserts.

Because this depends on the exact quote and parts list, Junior Andrew should not give final project-specific install instructions without routing the customer to build support.

TOUCH-UP PAINT CAUTION

If a customer asks about touch-up spray paint:

Touch-up paint is for slight scratches and blemishes on wood-grained aluminum material, not roof panels.

Do not recommend spraying directly from the can onto the material for small touch-ups.

General guidance:

“Spray a little paint into a cap or small container, then use a Q-tip or small brush to dab the scratch.”

BUILD STYLE

Do not give long step-by-step installation instructions unless the customer specifically asks for a general overview.

Do not act like a contractor or engineer.

Do not say “definitely cut here” or “definitely anchor here” for a customer’s specific build.

Do not replace build support.

Good wording:

“I can help you understand what the instructions are talking about, but I would follow your final design and parts checklist for the actual build.”

Good wording:

“That sounds like a project-specific install detail. If you already ordered, build support can pull up your exact design and walk you through it.”

Bad wording:

“Cut the part to this exact length.”

Bad wording:

“You definitely put the posts here.”

Bad wording:

“You do not need to call build support.”

Bad wording:

“All kits build the same way.”
""",

    "patio_cover_build_overview.txt": r"""
PATIO COVER BUILD OVERVIEW

This file gives Junior Andrew general patio cover build knowledge.

This is not a replacement for the customer’s final design, quote, engineering, parts checklist, or build support.

ATTACHED PATIO COVER BASICS

Attached patio covers connect to the house side using a hanger/channel or attachment system.

For attached solid covers, roof panels generally run from the house outward toward the front header.

The projection is the depth coming out from the house.

The length is the left-to-right dimension along the house.

The front header beam sits at the outside/front of the cover and is supported by posts.

A common layout idea:

- house side = hanger/channel
- front side = header beam and posts
- roof panels run from back to front
- projection = back-to-front direction
- length = side-to-side direction

FREESTANDING PATIO COVER BASICS

Freestanding covers do not use the house as the attachment reference.

For freestanding covers:

- the header beam sitting on top of the posts is the length
- the roof pans or rafters run front to back
- the front-to-back direction is the projection
- there is no house side to reference

If the customer is unsure which dimension is which, ask them which direction the header beam/post line runs and which way the roof panels or rafters run.

LATTICE COVER BASICS

Lattice covers are shade structures with open rafters/slats rather than a solid roof.

They are not designed to block rain the way a solid roof does.

Lattice kits are generally manufactured closer to exact lengths, but customers should still measure the material to confirm.

If a customer asks about electrical in lattice covers:

General concept only:

“Electrical can sometimes be run within rafters, and fans may require proper support or a wood insert, but exact electrical and support details should be confirmed with the customer’s design, local code, and build support.”

SOLID NON-INSULATED BASICS

Non-insulated solid covers use roof panels to create a solid shade/rain cover.

Non-insulated is not a lower-quality option than insulated.

It is a different application.

Non-insulated can make sense when the customer mainly wants a solid cover and does not need the specific benefits of insulated panels.

SOLID INSULATED BASICS

Insulated covers use thicker insulated roof panels.

Insulated can make sense when the customer cares about impact protection, walking on it for maintenance, hiding electrical, or possibly fully enclosing the patio later.

Do not call insulated an upgrade.

Do not say non-insulated is basic.

BUILD LAYOUT NOTE

For attached solid covers, make sure Junior Andrew understands the difference between cover length and total length.

The layout should be based on the cover length, which is the roof itself.

Total length may include additional cosmetic extension from wrap kits or end details.

Do not give final layout directions without telling the customer to check the final design.

AESTHETICS NOTE

Aluminum components may have a lock seam.

General idea:

- seams on 3x3 posts are often hidden by side plates
- seams on 2x6 and 3x8 material are often oriented so they are not visible from below

But do not give final install direction without telling the customer to follow the instructions and build support for their specific kit.

GENERAL BUILD ANSWER TEMPLATE

If asked “How hard is this to build?”:

“These are DIY kits, and many customers can build them with normal tools, but they are still custom enough that the final design and parts checklist matter. I can explain the general idea, but if you’ve already ordered, build support can pull up your exact design and give much better guidance.”

If asked “Do I have to cut material?”:

“For most non-insulated and insulated patio covers, some on-site trimming is expected because homes and slabs are not perfectly square. Lattice kits are generally closer to exact lengths, but it is still smart to measure everything before cutting.”

If asked “Can you walk me through the build?”:

“I can give a general overview, but I would not want to replace the actual instructions or build support. The safest path is to follow your final design, parts checklist, and the instruction packet for your exact product type.”
""",

    "brochure_product_knowledge.txt": r"""
BROCHURE PRODUCT KNOWLEDGE

This file summarizes customer-facing brochure and product knowledge for Junior Andrew.

PATIO KITS DIRECT GENERAL BROCHURE KNOWLEDGE

Patio Kits Direct sells do-it-yourself Alumawood patio cover kits.

Customer-facing benefits can include:

- cedar embossed aluminum that looks like wood
- low maintenance
- limited lifetime warranty depending on manufacturer/product details
- comprehensive build instructions
- live phone support during the build
- typical installation may take 1 to 2 days depending on the kit and customer situation
- product types include insulated, non-insulated, and lattice
- customers can use the 3D Designer Tool to design a cover

Do not overpromise installation time.

Say “typical installation may take 1 to 2 days” rather than guaranteeing it.

CUSTOMIZABLE OPTIONS

Common customizable options can include:

- decorative end caps
- rafter tails
- standard posts
- round columns
- square columns
- color options
- multi-color combinations
- fan beams
- recessed lights

Note:

Insulated panels may have more limited roof color availability depending on region/manufacturer.

Do not promise a specific color is available for every product or location unless the knowledge confirms it.

ALUMAWOOD PRODUCT KNOWLEDGE

Alumawood shade structures are aluminum shade structures with a wood-grain style.

Benefits can include:

- wood-look textured finish
- low maintenance compared with wood
- does not require painting like wood
- termite/insect resistance
- resistance to warping and cracking
- durable aluminum surface
- Aluma-Shield paint system
- designer colors
- matching fasteners
- optional recessed lighting system depending on product setup
- style options for beam/rafter end cuts such as beveled, mitered, corbel, and scallop

Do not overstate.

Do not say the customer will never need any maintenance at all.

Better:

“It is designed to be much lower maintenance than wood.”

LATTICE VS SOLID PRODUCT LANGUAGE

Lattice provides partial shade and an open shade-structure look.

Solid non-insulated provides more complete coverage from sun and rain than lattice.

Insulated is a solid roof option used for different applications such as impact protection, walking on it for maintenance, hiding electrical, and some enclosure situations.

Do not frame insulated as better quality.

Frame it as a different application.

WEATHERWOOD / DURALUM BROCHURE KNOWLEDGE

Weatherwood/Duralum brochure material describes patio cover options such as lattice, solid, fully insulated covers, or combinations.

The brochure references real-wood look and durability of aluminum.

Do not claim exact warranty terms unless the specific current warranty page confirms it.

If warranty comes up, route to current warranty details or a representative.

SALES STYLE

Junior Andrew should sound helpful and not like a brochure.

Good:

“Lattice is more about filtered shade and appearance. Solid non-insulated gives you a solid roof. Insulated is still a solid roof, but it can make more sense when impact protection, walking on it for maintenance, or hiding electrical matter.”

Bad:

“Our amazing products will transform your lifestyle.”

Bad:

“Insulated is the premium upgrade.”
""",

    "haven_lanais_reference.txt": r"""
HAVEN LANAIS REFERENCE

This file teaches Junior Andrew about Haven Lanais.

Haven Lanais are Patio Kits Direct’s fully enclosed lanai/enclosure options.

Haven Lanais should not be treated as standard patio covers.

Do not use standard patio cover build instructions to explain how to build a Haven Lanai.

Haven Lanais have their own product information and their own animated instructions from the 3D Designer.

GENERAL PRODUCT OVERVIEW

Haven Lanais are constructed using wood-grained aluminum roofing and framing.

Non-insulated and insulated roof/framing options may be available.

The windows and doors are 4-track vinyl units.

Door styles can include French doors or Cabana doors.

The vinyl window material gives a glass-like look at less cost than glass.

The 3D Patio Cover and Lanai Designer automatically calculates exact window and door sizing required for the customer’s dimensions and slope/pitch.

The 4-track vinyl windows can slide up or down to allow breezes in or help close the space.

Windows can come with screens and vinyl windows, or customers may be able to choose screens-only depending on options.

Customers can choose screen density options and vinyl tint options.

FLEXI-GLAZE VINYL

FlexiGlaze looks like glass, but it is not glass.

It is a transparent flexible vinyl membrane.

It helps protect from the elements and can handle certain impacts such as golf balls, baseballs, and even hail.

If bumped or pressed, the vinyl can return to shape.

Do not call it glass.

Good:

“It gives a glass-like look, but it is flexible vinyl, not glass.”

Bad:

“It uses glass windows.”

VENTILATION

Haven Lanai 4-track windows allow variable ventilation.

They can be closed, rolled down, rolled up, or left partially open.

This allows customers to adjust for breeze, view, or weather.

SCREENING

Top transom windows do not come with screens unless specifically requested in lieu of vinyl, and those top transom windows do not open.

All windows and doors can come with a screen and vinyl window option.

Customers may be able to opt for screens-only to remove vinyl windows, depending on options.

DIY / CUTTING MATERIAL

Haven Lanais are DIY products, but the customer will be required to cut material.

Many components may come overproduced because the build site may not be level, the house may not be square, or other install conditions may require extra length.

Some stock lengths may need to be cut.

Roof pans generally do not require cutting unless needed to center electrical in the design.

Animated Instructions can guide the customer through what to cut and where to place it.

Live build support is available if needed.

Do not make the Lanai sound like no cutting is required.

Do not use standard patio cover instructions as the Lanai build guide.

AVERAGE COST COMPARISON LANGUAGE

The Haven Lanai informational deck includes average nationwide comparison examples showing DIY vinyl 4-track Haven Lanais as lower-cost than average installed 3-season and 4-season sunrooms for example sizes.

Use this carefully.

Do not give exact pricing unless current pricing is confirmed.

Do not quote these numbers as a live quote.

Better:

“The product information shows Haven Lanais are designed to be a more affordable DIY alternative to many installed sunroom options, but exact pricing still needs to come from a representative or the designer.”

WHY HAVEN LANAIS CAN BE MORE AFFORDABLE

Reasons can include:

- high-quality vinyl instead of glass windows
- DIY kit model instead of specialized installers
- wood-grained aluminum frame giving a wood-like look with lower material cost

WINDOW AND DOOR SPECIFICATIONS

Lanai Cabana Door width range: 32 inches to 36 inches.

Lanai French Door width range: 64 inches to 72 inches.

Lanai Door height: 80 inches.

Lanai Window width range: 12 inches to 65 inches.

Lanai Window height range: 32 inches to 110 inches.

Do not treat these as final design limits for a specific customer without routing to the 3D Designer or a representative.

TRANSOM WINDOWS

Transom windows may be added depending on:

- roof slope/pitch
- concrete slab slope/pitch
- structure height

Transom windows help accommodate changes in pitch and can add an upgraded look.

COLORS

Available roof colors can depend on:

- region
- manufacturer
- product selected
- non-insulated vs insulated

Frame/trim refers to:

- header beam
- rafters
- posts
- windows
- doors

Roof color is chosen separately and may vary depending on location.

Some frame/trim colors are available nationwide and others are region-specific.

Do not promise exact color availability without checking the current design/region.

PERMITTING

For Haven Lanais, the structural portion includes the patio cover roof, posts, beams, and rafters.

Patio Kits Direct provides structural engineering for this structure based on the customer’s city snow load, wind speed, and seismic conditions.

Engineering documents are provided free with the purchase of the kit.

The vinyl windows and doors are considered added accessories to the structure and do not affect the engineering integrity.

Permitting documentation is not provided for the window portion of the lanai.

Junior Andrew is not an engineer.

Do not promise that a design will pass permit.

CARE AND CLEANING

Do not use a hose or pressure washer to clean Haven Lanai vinyl windows.

Remember: vinyl is not glass.

Use careful cleaning language.

If unsure, tell the customer to follow the care instructions and ask support.

BUILD INSTRUCTIONS

If a customer asks how to build their Haven Lanai:

Do not use patio cover build instructions.

Say:

“Haven Lanais have their own animated instructions in the 3D Designer for the customer’s custom lanai. Open the design, go to the menu, select Animated Instructions, and review the steps there. Build support can also help if you’ve already ordered.”

The animated instructions allow customers to:

- review the build step by step
- toggle between menu items
- slow down or speed up animation
- pause
- go step by step manually
- lock an angle/perspective
- loop instructions
- keep track of the current step

GOOD CUSTOMER ANSWERS

If asked “What is a Haven Lanai?”:

“A Haven Lanai is Patio Kits Direct’s fully enclosed lanai option. It uses wood-grained aluminum roofing/framing with 4-track vinyl windows and doors, so it gives you an enclosed room feel without being a traditional glass sunroom.”

If asked “Are the windows glass?”:

“No, they look like glass, but they are flexible vinyl. That helps keep the system lighter and more affordable than a traditional glass sunroom.”

If asked “Can I build it myself?”:

“Yes, it is designed as a DIY kit, but you should expect to cut some material and follow the custom animated instructions from the 3D Designer. If you’ve already ordered, build support can help with your specific design.”

If asked “Do I use the patio cover instructions?”:

“No. Haven Lanais have their own animated instructions from the 3D Designer. I would not use standard patio cover build instructions to explain a Lanai build.”
""",

    "haven_lanai_slope_reference.txt": r"""
HAVEN LANAI SLOPE REFERENCE

This file teaches Junior Andrew about concrete slab slope/pitch for Haven Lanais.

Concrete slab slope is very important for Haven Lanais because it affects window sizing and layout.

The 3D Designer uses the customer’s dimensions and slope/pitch to calculate window and door sizes.

WHY SLOPE MATTERS

The slope/pitch of the concrete slab can determine the quantity and size of windows on the left and right sides of the Lanai along the projection.

Example from the product information:

For a 10 by 20 Lanai:

- 0 inch pitch can accommodate two 50 inch windows lined evenly
- 3/8 inch pitch may require three 30 inch windows with staggered heights

Do not promise exact window layout without the 3D Designer.

Say:

“The designer uses the slope to calculate the correct window sizing, so it matters a lot for Haven Lanais.”

HOW TO MEASURE CONCRETE SLOPE

General method:

1. Anchor a string exactly where the concrete meets the house at the corner.
2. Keep the string perfectly level using a bubble level.
3. Measure exactly 120 inches, or 10 feet, out from the house.
4. At the 10 foot mark, measure vertically straight down from the level string to the concrete.
5. That vertical measurement is the rise/drop over a 10 foot run.
6. Slope equals rise divided by run.

Example:

- rise = 2 inches
- run = 120 inches
- slope = 2 divided by 120 = 0.0167
- that equals about 1/8 inch per foot

Important:

Do not lay the string directly on the concrete.

Keep it level.

Measure straight down vertically at the 10 foot mark.

RECOMMENDED SLOPE GUIDANCE

The slope guide says:

- 1/8 inch per foot is ideal
- 1/4 inch per foot is maximum typical
- less than 1/8 inch per foot can create potential drainage issues

Use this as general guidance.

If the customer is unsure, tell them the design team can calculate this for them.

PHONE NUMBER

If the customer is still unsure, Patio Kits Direct can help:

(888) 851-8351

GOOD CUSTOMER ANSWER

If asked “How do I measure the slope of my slab?”:

“Use a level string. Anchor it where the concrete meets the house, keep the string perfectly level, measure exactly 10 feet out from the house, then measure straight down from the string to the concrete at that 10 foot mark. That vertical measurement tells you the rise/drop over 10 feet. For example, 2 inches over 120 inches works out to about 1/8 inch per foot.”

If asked “Why does slab slope matter for a Haven Lanai?”:

“For Haven Lanais, slab slope affects the window sizing and layout, especially on the projection sides. The 3D Designer uses that slope to calculate the correct windows and transoms, so it’s important to enter it as accurately as possible.”

If asked “What if I can’t measure it?”:

“No problem. If you’re unsure, the design team can help calculate it. It’s better to double-check than guess, because slope affects the window layout.”
"""
}

for name, content in files.items():
    (KNOWLEDGE / name).write_text(content.strip() + "\n", encoding="utf-8")

new_entries = [
    '    BASE_DIR / "knowledge" / "build_instruction_guardrails.txt",',
    '    BASE_DIR / "knowledge" / "patio_cover_build_overview.txt",',
    '    BASE_DIR / "knowledge" / "brochure_product_knowledge.txt",',
    '    BASE_DIR / "knowledge" / "haven_lanais_reference.txt",',
    '    BASE_DIR / "knowledge" / "haven_lanai_slope_reference.txt",',
]

app_text = APP_FILE.read_text(encoding="utf-8")

if "build_instruction_guardrails.txt" not in app_text:
    marker = "    BASE_DIR / \"knowledge\" / \"wording_overrides.txt\",\n"
    insert_text = marker + "\n".join(new_entries) + "\n"
    app_text = app_text.replace(marker, insert_text)

APP_FILE.write_text(app_text, encoding="utf-8")

print("DONE")
print(f"Backup created at: {backup_dir}")
print("Knowledge files created/updated:")
for name in files:
    print(f"- {name}")
print("App knowledge list updated.")