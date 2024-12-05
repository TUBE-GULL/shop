async function fetchProducts() {
    try {
        const response = await fetch('/shop/products');
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

function displayProducts(products) {
    const shopContainer = document.getElementById('products');
    shopContainer.innerHTML = '';

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';

        productCard.innerHTML = `
            <img src="${product.image_url}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>Price: $${product.price}</p>
            <button onclick="addToCart(${product.id})">Add to Cart</button>
        `;

        shopContainer.appendChild(productCard);
    });
}


function addToCart(productId) {
    console.log(`Product ${productId} added to cart`);
}

fetchProducts();