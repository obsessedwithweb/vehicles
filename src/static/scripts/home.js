// home.js

function toggleCart() {
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    if (sidebar && overlay) {
        sidebar.classList.toggle('active'); 
        overlay.classList.toggle('active');
    } else {
        console.error("Cart sidebar or overlay element not found.");
    }
}

function goToShop() {
    console.log("Returning to shop...");
    toggleCart();
}

document.addEventListener("DOMContentLoaded", function () {
    // Mobile menu dropdown toggle
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const dropbtn = dropdown.querySelector('.dropbtn');
        
        if (dropbtn) {
            dropbtn.addEventListener('click', function(e) {
                e.preventDefault();
                // Check if we're on mobile
                if (window.innerWidth <= 768) {
                    dropdown.classList.toggle('active');
                }
            });
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            dropdowns.forEach(dropdown => {
                const dropbtn = dropdown.querySelector('.dropbtn');
                if (!dropdown.contains(e.target) && dropbtn !== e.target) {
                    dropdown.classList.remove('active');
                }
            });
        }
    });

    // --- About Section ---
    const experienceData = {
        image: "site/img/about.jpg",
        subheader: "Welcome to Our Boutique Autosupply",
        description: "At AutoSupply, we aim to simplify the process of finding high-quality, affordable vehicle spare parts. Our mission is to provide a convenient and reliable platform, ensuring vehicle owners and repair shops have access to the best products with excellent customer service.",
        buttonText: "Read More",
        buttonLink: "#" 
    };

    const imageElement = document.getElementById("image");
    const subheaderElement = document.getElementById("subheader");
    const descriptionElement = document.getElementById("description");
    const btnElement = document.getElementById("btn");


    if (subheaderElement) subheaderElement.textContent = experienceData.subheader;
    if (descriptionElement) descriptionElement.textContent = experienceData.description;
    if (btnElement) {
        btnElement.textContent = experienceData.buttonText;
        btnElement.href = experienceData.buttonLink;
    }

    // --- Blog Section ---

    /*
    const blogPosts = [
    //      {
    //          title: "The importance of spare parts in Truck maintenance.",
    //          date: "March 12, 2025",
    //          category: "Trucks",
    //          image: "site/img/blog-1.jpg",
    //          link: "#"
    //      },
    //      {
    //          title: "Your Trusted Source for Vehicle Parts.",
    //          date: "March 12, 2025",
    //          category: "Motors",
    //          image: "site/img/blog-2.jpg",
    //          link: "#"
    //      },
    //      {
    //          title: "How to choose the right spare parts for your car.",
    //          date: "March 12, 2025",
    //          category: "Cars",
    //          image: "site/img/blog-3.jpg",
    //          link: "#"
    //      },
    //      {
    //          title: "The future of car spare parts: Trends and Innovations.",
    //          date: "March 12, 2025",
    //          category: "Cars",
    //          image: "site/img/blog-4.jpg",
    //          link: "#"
    //      },
    //      {
    //          title: "The role of mechanics in the Automative Industry.",
    //          date: "March 12, 2025",
    //          category: "Mechanic",
    //          image: "site/img/blog-5.jpg",
    //          link: "#"
    //      }
      ];


      function renderBlogPosts(posts) {
          const lis =  [...document.querySelectorAll(".blog-card")]
          lis.forEach(post => {
              blogCard.innerHTML = `
                <div class="card-banner">
                  <a href="${post.link}">
                    <img src="${post.image}" alt="${post.title}" loading="lazy" class="w-100">
                  </a>
                  <a href="#" class="btn card-badge">${post.category}</a>
                </div>
                <div class="card-content">
                  <h3 class="h3 card-title"><a href="${post.link}">${post.title}</a></h3>
                  <div class="card-meta">
                    <div class="publish-date">
                      <ion-icon name="time-outline"></ion-icon>
                      <time datetime="${post.date}">${post.date}</time> <!-- Use actual date for datetime -->
                    </div>
                
                  </div>
                </div>
              `;
              blogList.appendChild(blogCard);
          });
      }*/

    //  renderBlogPosts(blogPosts);
    const serviceData = [
        {
            image: 'site/img/ser-1.jpg',
            title: 'High-Quality Spare Parts',
            description: 'Premium, durable parts from trusted brands for long-lasting performance and safety.'
        },
        {
            image: 'site/img/ser-2.jpg',
            title: 'Professional Installation & Usage Assistance',
            description: 'Expert guidance on product installation and usage with professional mechanics.'
        },
        {
            image: 'site/img/ser-3.jpg',
            title: 'Dedicated Customer Support',
            description: 'A responsive team to assist, answer inquiries, and help find the perfect spare parts.'
        },
        {
            image: 'site/img/ser-4.jpg',
            title: 'Fast & Reliable Delivery',
            description: 'We ensure quick, secure delivery to get your spare parts on time and minimize vehicle downtime.'
        }
    ];

    //  Services

    //  const serviceGrid = document.getElementById('service-grid');

    //   if (serviceGrid) {
    //       serviceData.forEach(service => {
    //           const serviceCard = document.createElement('div');
    //           serviceCard.classList.add('service__card'); 

    //           const serviceImage = document.createElement('img');
    //           serviceImage.src = service.image;
    //           serviceImage.alt = service.title;
    //           serviceImage.loading = 'lazy'; 

    //           const serviceTitle = document.createElement('h4');
    //           serviceTitle.textContent = service.title;

    //           const serviceDescription = document.createElement('p');
    //           serviceDescription.textContent = service.description;

    //           serviceCard.appendChild(serviceImage);
    //           serviceCard.appendChild(serviceTitle);
    //           serviceCard.appendChild(serviceDescription);

    //           serviceGrid.appendChild(serviceCard);
    //       });
    //       const observer = new IntersectionObserver((entries, observer) => {
    //           entries.forEach(entry => {
    //               if (entry.isIntersecting) {
    //                   entry.target.classList.add('visible');
    //                   observer.unobserve(entry.target);
    //               }
    //           });
    //       }, {
    //           threshold: 0.1 
    //       });

    //       const serviceCards = document.querySelectorAll('.service__card');
    //       serviceCards.forEach(card => {
    //           observer.observe(card);
    //       });

    //   } else {
    //       console.error("Element with ID 'service-grid' not found.");
    //   }

    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            // Remove active class from all dropdowns when returning to desktop
            dropdowns.forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });
});