// Handling the hamburger menu

const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav_links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', function(){
    navLinks.classList.toggle('nav_open');
  });
}

// Copying product info in the Clipboard

document.querySelectorAll(".copy_caption_btn").forEach(function (button) {
  button.addEventListener("click", function () {
    const name = button.dataset.name;
    const price = button.dataset.price;
    const description = button.dataset.description;

    const caption = `product Name: ${name}\nprice: ${price}\ndescription: ${description}`;
    navigator.clipboard.writeText(caption);
  });
});

// Creating  new input rows for  variants

const addVariantBtn = document.getElementById("add_variant_btn");
if (addVariantBtn) {
  addVariantBtn.addEventListener("click", function () {
    const newRowHTML = `
    <div class="form_row">
        <div class="form_field">
            <label>Size:</label>
            <input name="size[]">
        </div>
        <div class="form_field">
            <label>Color:</label>
            <input name="color[]">
        </div>
    </div>        
    `;
    document
      .getElementById("variant_rows")
      .insertAdjacentHTML("beforeend", newRowHTML);
  });
}
// Creating  new input rows for  images

const addImageBtn = document.getElementById("add_image_btn");
if (addImageBtn) {
  addImageBtn.addEventListener("click", function () {
    const newRowHTML = `
    <div class="form_row">
            <label>Image URL:</label>
            <input type="file" name="image_file[]"/>
    </div>        
    `;
    document
      .getElementById("image_row")
      .insertAdjacentHTML("beforeend", newRowHTML);
  });
}

// Reading selected product and variant from the existing products in a dropdown

const productSelect = document.getElementById("product_select");
const variantsSelect = document.getElementById("variants");
const hiddenName = document.getElementById("hidden_product_name");
const hiddenSize = document.getElementById("hidden_product_size");
const hiddenColor = document.getElementById("hidden_product_color");
const hiddenPrice = document.getElementById("hidden_price");

if (productSelect && variantsSelect && hiddenName && hiddenSize && hiddenColor && hiddenPrice) {
  productSelect.addEventListener("change", function () {
    const productId = productSelect.value;
    const selectedOption = productSelect.options[productSelect.selectedIndex];
    const productName = selectedOption.dataset.name;
    hiddenName.value = productName;

    fetch(`/admin/api/variants/${productId}`)
      .then((response) => response.json())
      .then((data) => {
        variantsSelect.innerHTML = "";
        data.forEach((variant) => {
          const option = document.createElement("option");
          option.value = variant.id;
          option.textContent = `size:${variant.size} - color:${variant.color} - price: KSh ${variant.price}`;
          option.dataset.size = variant.size;
          option.dataset.color = variant.color;
          option.dataset.price = variant.price;
          variantsSelect.appendChild(option);
        });
        updateVariantHiddenFields();
      });
  });

  variantsSelect.addEventListener('change', updateVariantHiddenFields);
  function updateVariantHiddenFields() {
    const selectedOption = variantsSelect.options[variantsSelect.selectedIndex];
    const size = selectedOption.dataset.size;
    const color = selectedOption.dataset.color;
    const price = selectedOption.dataset.price;
    hiddenSize.value = size;
    hiddenColor.value = color;
    hiddenPrice.value = price;
}
}