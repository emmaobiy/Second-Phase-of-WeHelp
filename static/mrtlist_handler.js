window.addEventListener('DOMContentLoaded', fetchMRTList);

// 獲取 MRT 
async function fetchMRTList(){
    try {
        const response=await fetch('/api/mrts');
        const data=await response.json();
        renderMRTList(data.data);
    } catch (error) {
        console.error('MRT列表獲取失敗:', error);
    }
}

// 呈現 MRT 
function renderMRTList(mrtNames){
    const mrtListContainer=document.getElementById('mrt-list');
    mrtListContainer.innerHTML='';

    mrtNames.forEach(mrtName =>{
        const mrtElement=document.createElement('div');
        mrtElement.textContent=mrtName;
        mrtElement.classList.add('mrt-station'); 
        mrtElement.addEventListener('click', handleMRTClick);
        mrtListContainer.appendChild(mrtElement);
    });
}

// 左右滾動
const leftButton=document.querySelector('.mrt-list-button-left');
const rightButton=document.querySelector('.mrt-list-button-right');
const mrtList=document.getElementById('mrt-list');

leftButton.addEventListener('click', ()=>{
    mrtList.scrollLeft-=mrtList.offsetWidth*0.8; 
});

rightButton.addEventListener('click', ()=>{
    mrtList.scrollLeft+=mrtList.offsetWidth*0.8; 
});

// 點擊 MRT
function handleMRTClick(event){
    const container=document.getElementById('attractions-container');
    container.innerHTML='';

    const clickedMRT=event.target.textContent;
    const keywordInput=document.getElementById('keyword');
    keywordInput.value=clickedMRT;
    page=0; 

    handleSearchSubmit(new Event('submit'));
}

