document.querySelectorAll('.copy_caption_btn').forEach(function(button){
    button.addEventListener('click', function(){
    const name = button.dataset.name;
    const price = button.dataset.price;
    const description = button.dataset.description;

    const caption = `product Name: ${name}\nprice: ${price}\ndescription: ${description}`;
    navigator.clipboard.writeText(caption);
    });
});

document.getElementById('add_variant_btn').addEventListener('click', function(){
    const newRowHTML = `
    <div class="form_row">
        <div class="form_field">
            <lable>Size:</lable>
            <input name="size"[]">
        </div>
        <div class="form_field">
            <lable>Color:</lable>
            <input name="color[]">
        </div>
    </div>        
    `;
    document.getElementById('variant_rows').insertAdjacentHTML('beforeend', newRowHTML);
});
document.getElementById('add_image_btn').addEventListener('click', function(){
    const newRowHTML = `
    <div class="form_row">
            <lable>Image URL:</lable>
            <input type="file" name="image_file[]"/>
    </div>        
    `;
    document.getElementById('image_row').insertAdjacentHTML('beforeend', newRowHTML);
});