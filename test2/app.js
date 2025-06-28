document.addEventListener('DOMContentLoaded', function() {
    const sidebarContainer = document.getElementById('sidebar');
    if (!sidebarContainer) return; // Do not run if the sidebar element doesn't exist

    // The entire sidebar HTML structure.
    const sidebarHTML = `
        <div class="logo-container">
            <a href="index.html" class="logo">
                <img src="https://placehold.co/50x50/6366f1/white?text=ST" alt="Logo">
                <span>Student Tracker</span>
            </a>
            <button onclick="toggleSidebar()" id="toggle-btn">
                <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"><path d="m313-480 155 156q11 11 11.5 27.5T468-268q-11 11-28 11t-28-11L228-452q-6-6-8.5-13t-2.5-15q0-8 2.5-15t8.5-13l184-184q11-11 27.5-11.5T468-692q11 11 11 28t-11 28L313-480Zm264 0 155 156q11 11 11.5 27.5T732-268q-11 11-28 11t-28-11L492-452q-6-6-8.5-13t-2.5-15q0-8 2.5-15t8.5-13l184-184q11-11 27.5-11.5T732-692q11 11 11 28t-11 28L577-480Z"/></svg>
            </button>
        </div>
        <nav>
            <ul>
                <li><a href="index.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M240-200h120v-200q0-17 11.5-28.5T400-440h160q17 0 28.5 11.5T600-400v200h120v-360L480-740 240-560v360Zm-80 0v-360q0-19 8.5-36t23.5-28l240-180q21-16 48-16t48 16l240 180q15 11 23.5 28t8.5 36v360q0 33-23.5 56.5T720-120H560q-17 0-28.5-11.5T520-160v-200h-80v200q0 17-11.5 28.5T400-120H240q-33 0-56.5-23.5T160-200Zm320-270Z"/></svg><span>Dashboard</span></a></li>
                <li><a href="assignments.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M280-280h400v-80H280v80Zm0-160h400v-80H280v80Zm0-160h400v-80H280v80ZM160-120q-33 0-56.5-23.5T80-200v-560q0-33 23.5-56.5T160-840h640q33 0 56.5 23.5T880-760v560q0 33-23.5 56.5T800-120H160Zm0-80h640v-560H160v560Z"/></svg><span>Assignments</span></a></li>
                <li><a href="classes.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M480-240 200-400l280-160 280 160-280 160Zm0-200L200-600l280-160 280 160-280 160Zm0 200L200-400l280-160 280 160-280 160Zm0-200L200-600l280-160 280 160-280 160ZM120-280v-400q0-24 12-45t32-35l280-160q19-11 40-11t40 11l280 160q20 14 32 35t12 45v400q0 24-12 45t-32 35L520-120q-19 11-40 11t-40-11L164-200q-20-14-32-35t-12-45Zm80 20 280 160 280-160v-400L480-680 200-520v400Z"/></svg><span>Classes</span></a></li>
                <li><a href="calendar.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M200-80q-33 0-56.5-23.5T120-160v-560q0-33 23.5-56.5T200-800h40v-80h80v80h320v-80h80v80h40q33 0 56.5 23.5T840-720v560q0 33-23.5 56.5T760-80H200Zm0-80h560v-400H200v400Zm0-480h560v-80H200v80Zm0 0v-80 80Z"/></svg><span>Calendar</span></a></li>
                <li><a href="grades.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M240-200h120v-480H240v480Zm240 0h120v-320H480v320Zm240 0h120v-160H720v160ZM120-120q-33 0-56.5-23.5T40-200v-560q0-33 23.5-56.5T120-840h720q33 0 56.5 23.5T920-760v560q0 33-23.5 56.5T840-120H120Z"/></svg><span>Grades</span></a></li>
                <li>
                    <button onclick="toggleSubMenu(this)" class="dropdown-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="m300-300 280-80 80-280-280 80-80 280Zm180-120q-25 0-42.5-17.5T420-480q0-25 17.5-42.5T480-540q25 0 42.5 17.5T540-480q0 25-17.5 42.5T480-420Zm0 340q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q133 0 226.5-93.5T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 133 93.5 226.5T480-160Zm0-320Z"/></svg>
                        <span>Explore</span>
                        <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M480-361q-8 0-15-2.5t-13-8.5L268-556q-11-11-11-28t11-28q11-11 28-11t28 11l156 156 156-156q11-11 28-11t28 11q11 11 11 28t-11 28L508-372q-6 6-13 8.5t-15 2.5Z"/></svg>
                    </button>
                    <ul class="sub-menu">
                        <li><a href="request.html"><span>Request Form</span></a></li>
                        <li><a href="ai.html"><span>Interlink AI</span></a></li>
                        <li><a href="tutoring.html"><span>Tutoring</span></a></li>
                        <li><a href="tools.html"><span>Productivity Tools</span></a></li>
                        <li><a href="qotd.html"><span>Question of the Day</span></a></li>
                    </ul>
                </li>
                <li><a href="canvas.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M480-262q66 0 126-30.5T682-363l-45-78q-36 21-75 31.5t-82 10.5q-96 0-165-68.5T240-630q0-94 69-162.5t167-68.5q43 0 83.5 12.5T610-820l46-76q-47-28-98.5-42T480-950q-134 0-228 92.5T160-630q0 134 94 227t226 93Zm16-19L658-417q35-64 53-128.5T729-679l-117-68q-5 19-9.5 37.5T598-571q-15 67-62 113.5T418-393l78 112Z"/></svg><span>Canvas</span></a></li>
                <li id="tyler-nav-link"><a href="tyler.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="m382-331 161-68 68-161-161 68-68 161Zm65-103q-21 0-36.5-15.5T395-486q0-21 15.5-36.5T447-538q21 0 36.5 15.5T499-486q0 21-15.5 36.5T447-434Zm33 354q-70 0-132-26.5T237-183q-45-45-71.5-107T139-422q0-70 26.5-132T237-665q45-45 107-71.5T447-763q70 0 132 26.5T690-665q45 45 71.5 107T793-422q0 70-26.5 132T690-183q-45 45-107 71.5T480-80Zm0-66q111 0 188.5-77.5T746-422q0-111-77.5-188.5T480-688q-111 0-188.5 77.5T214-422q0 111 77.5 188.5T480-146Zm0-276Z"/></svg><span>Tyler</span></a></li>
                <li><a href="qbank.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M560-360q17 0 29.5-12.5T602-402q0-17-12.5-29.5T560-444q-17 0-29.5 12.5T518-402q0 17 12.5 29.5T560-360Zm-30-128h60q0-29 6-42.5t28-35.5q30-30 40-48.5t10-43.5q0-45-31.5-73.5T560-760q-41 0-71.5 23T446-676l54 22q9-25 24.5-37.5T560-704q24 0 39 13.5t15 36.5q0 14-8 26.5T578-596q-33 29-40.5 45.5T530-488ZM320-240q-33 0-56.5-23.5T240-320v-480q0-33 23.5-56.5T320-880h480q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H320Zm0-80h480v-480H320v480ZM160-80q-33 0-56.5-23.5T80-160v-560h80v560h560v80H160Zm160-720v480-480Z"/></svg><span>Q-Bank</span></a></li>
                <li><a href="profile.html"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M480-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM160-240v-32q0-34 17.5-62.5T224-378q62-31 126-46.5T480-440q66 0 130 15.5T736-378q29 15 46.5 43.5T800-272v32q0 33-23.5 56.5T720-160H240q-33 0-56.5-23.5T160-240Zm80 0h480v-32q0-11-5.5-20T700-306q-54-27-109-40.5T480-360q-56 0-111 13.5T260-306q-9 5-14.5 14t-5.5 20v32Zm240-320q33 0 56.5-23.5T560-640q0-33-23.5-56.5T480-720q-33 0-56.5 23.5T400-640q0 33 23.5 56.5T480-560Zm0-80Zm0 400Z"/></svg><span>Credits</span></a></li>
            </ul>
        </nav>
    `;
    
    sidebarContainer.innerHTML = sidebarHTML;

    // --- Active Page Logic ---
    const currentPage = window.location.pathname.split("/").pop() || 'index.html';
    const navLinks = sidebarContainer.querySelectorAll('nav a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.parentElement.classList.add('active');
            const subMenu = link.closest('.sub-menu');
            if (subMenu) {
                subMenu.style.maxHeight = subMenu.scrollHeight + "px";
                subMenu.previousElementSibling.parentElement.classList.add('active');
            }
        }
    });

    // --- Tyler Tab Easter Egg Logic ---
    let canvasClickStreak = 0;
    const tylerNavLink = document.getElementById('tyler-nav-link');

    // Check if unlocked on page load
    if (localStorage.getItem('tylerUnlocked') === 'true') {
        tylerNavLink.style.display = 'block';
    }
    
    document.body.addEventListener('click', (e) => {
        const targetLink = e.target.closest('a');
        if (!targetLink) return;

        if (targetLink.getAttribute('href') === 'canvas.html') {
            canvasClickStreak++;
        } else {
            canvasClickStreak = 0; // Reset streak if any other link is clicked
        }
        
        if (canvasClickStreak >= 3) {
            if (localStorage.getItem('tylerUnlocked') !== 'true') {
                 tylerNavLink.style.display = 'block';
                 localStorage.setItem('tylerUnlocked', 'true');
                 alert('🐝 Tyler tab unlocked! 🐝');
            }
        }
    }, true); // Use capture phase to catch the click before navigation
;

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

function toggleSubMenu(button) {
    const subMenu = button.nextElementSibling;
    const isOpening = !subMenu.style.maxHeight;
    
    // Close all sub-menus first
    document.querySelectorAll('.sub-menu').forEach(menu => {
        menu.style.maxHeight = null;
    });

    // If we are opening a new one, set its max-height
    if (isOpening) {
        subMenu.style.maxHeight = subMenu.scrollHeight + "px";
    }
}
 }
)