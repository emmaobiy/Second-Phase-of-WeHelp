function getIDfromURL() {
    const path = window.location.pathname;
    const match = path.match(/\/attraction\/(\d+)/);
    return parseInt(match[1], 10);
}


async function fetchAttractionDetails(attractionId) {
    const response = await fetch(`/api/attraction/${attractionId}`);
    const data = await response.json();
    
    if (response.ok) {
        renderAttractionDetails(data.data);
    } else {
        console.error('獲取景點詳細資訊時發生錯誤:', response.statusText);
        window.location.href = '/';
    }
}


function preloadFirstImage(imageUrl) {
    return new Promise((resolve, reject) => {
        const img=new Image();
        img.onload=() => resolve(img);
        img.onerror=() => reject(new Error(`Failed to load image: ${imageUrl}`));
        img.src=imageUrl;
    });
}

function renderAttractionDetails(attraction) {
    const attractionNameElement=document.getElementById('attraction-name');
    const attractionCat_MRTElement=document.getElementById('attraction-cat-mrt');
    const attractionIntroductionElement=document.getElementById('attraction-introduction');
    const attractionAddressElement=document.getElementById('attraction-address');
    const attractionTransportElement=document.getElementById('attraction-transportation');
    const pictureContainer=document.getElementById('attraction-picture-container');
    const leftButton=document.getElementById('attraction-picture-button-left');
    const rightButton=document.getElementById('attraction-picture-button-right');
    const circleButtonsContainer=document.getElementById('attraction-picture-buttons-circle-container');

    if (!attractionNameElement || !attractionCat_MRTElement || !attractionIntroductionElement ||
        !attractionAddressElement || !attractionTransportElement || !pictureContainer ||
        !leftButton || !rightButton || !circleButtonsContainer) {
        console.error('缺少ElementId');
        return;
    }

    attractionNameElement.textContent=attraction.name || '';
    attractionCat_MRTElement.textContent=`${attraction.cat || ''} at ${attraction.mrt || ''}`;
    attractionIntroductionElement.textContent=attraction.description || '';
    attractionAddressElement.textContent=attraction.address || '';
    attractionTransportElement.textContent=attraction.transport || '';

    const attractionImages=Array.isArray(attraction.images) ? attraction.images : [];

    let currentImageIndex=0;

    function updateImage(index) {
        if (!circleButtonsContainer || !circleButtonsContainer.children) {
            return;
        }
        if (index < 0 || index >= attractionImages.length) {
            return;
        }
        const imageUrl=attractionImages[index];
        pictureContainer.style.backgroundImage=`url('${imageUrl}')`;

        const circleButtons=circleButtonsContainer.children;
        for (let i=0; i < circleButtons.length; i++) {
            const button=circleButtons[i];
            if (i === index) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        }
    }

    if (attractionImages.length > 0) {
        preloadFirstImage(attractionImages[0]).then(() => {
            updateImage(currentImageIndex);
        }).catch((error) => {
            console.error('圖片預載失敗:', error);
        });

        leftButton.addEventListener('click', function() {
            currentImageIndex=(currentImageIndex - 1 + attractionImages.length) % attractionImages.length;
            updateImage(currentImageIndex);
        });

        rightButton.addEventListener('click', function() {
            currentImageIndex=(currentImageIndex + 1) % attractionImages.length;
            updateImage(currentImageIndex);
        });

        circleButtonsContainer.innerHTML='';

        for (let idx=0; idx < attractionImages.length; idx++) {
            const circleButton=document.createElement('button');
            circleButton.classList.add('attraction-picture-button-circle');
            if (idx === 0) {
                circleButton.classList.add('active');
            }
            circleButton.addEventListener('click', function() {
                currentImageIndex=idx;
                updateImage(currentImageIndex);
            });
            circleButtonsContainer.appendChild(circleButton);
        }
    }
}

window.addEventListener('DOMContentLoaded', function() {
    const attractionId = getIDfromURL();
    fetchAttractionDetails(attractionId);
});

