from enum import Enum


class Model(Enum):
    MODEL_1 = 1
    MODEL_2 = 2

class CardSide(Enum):
    FRONT = 1
    BACK = 2


def generate_card_side(model: Model, card_side: CardSide):
    style_content = open("model_style.css").read()
    script_front_content = open("model_front_script.js").read()
    script_back_content = open("model_back_script.js").read()

    model_media_back_wrapper = open("model_back_media_wrapper.mustache").read()
    model_front_media_wrapper = open("model_front_media_wrapper.mustache").read()

    model1_front_top = open("model1_front_top.mustache").read()
    model1_back_top = open("model1_back_top.mustache").read()

    model2_front_top = open("model2_front_top.mustache").read()
    model2_back_top = open("model2_back_top.mustache").read()
    match (model, card_side):
        case (Model.MODEL_1, CardSide.FRONT):
            return f"""
<style>
{style_content}
</style>

<div class="card-container">
	{model1_front_top}
    {model_front_media_wrapper}
</div>

<script>
{script_front_content}
</script>
"""
        case (Model.MODEL_2, CardSide.FRONT):
            return f"""
<style>
{style_content}
</style>

<div class="card-container">
    {model2_front_top}
    {model_front_media_wrapper}
</div>

<script>
{script_front_content}
</script>
"""
        case (Model.MODEL_1, CardSide.BACK):
            return f"""
<style>
{style_content}
</style>

<div class="card-container">
    {model1_back_top}
    {model_media_back_wrapper}
</div>

<script>
{script_back_content}
</script>
"""
        case (Model.MODEL_2, CardSide.BACK):
            return f"""
<style>
{style_content}
</style>

<div class="card-container">
    {model2_back_top}
    {model_media_back_wrapper}
</div>

<script>
{script_back_content}
</script>
"""
    return None