import re

with open('homepage.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Favicon
content = content.replace('<!-- // Stylesheets // -->', '<!-- // Favicon // -->\n<link rel="icon" href="/images/logo.png" type="image/png" />\n<!-- // Stylesheets // -->')

# 2. Nav
old_nav = '''      <div class="logo-text">
        <span class="logo-title">University of<br/>Karachi</span>
        <span class="logo-subtitle">SINCE 1951 &middot; KARACHI, PAKISTAN</span>
      </div>
    </a>
    <div id="nav">
      <ul>
        <li><a href="/welcome-address.php">About</a></li>'''

new_nav = '''    </a>
    <div id="nav">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/welcome-address.php">About</a></li>'''

content = content.replace(old_nav, new_nav)

# 3. History
old_academics = '''<!-- New Academics Section -->
    <div class="academics_section">
        <div class="academics_intro">
            <h2>Eight faculties. Fifty-three departments.</h2>'''

new_academics = '''<!-- New Our History Section -->
    <div class="history_section">
        <div class="history_left">
            <div class="section_label">OUR HISTORY</div>
            <h2>Established by an act of parliament, seventy-five years ago.</h2>
            
            <p>The University of Karachi was founded under the Karachi University Act, passed on 23 October 1950 and enacted the following year, with Prof. A. B. A. Haleem appointed as its first Vice Chancellor. For its first two years the university existed only to examine the students of Sindh's affiliated colleges &mdash; it began teaching its own students in 1953, opening with two faculties and an intake of fifty.</p>
            
            <p>As the young university outgrew its buildings beside Civil Hospital, a 1,279-acre plot on what is now University Road was acquired, and on 18 January 1960 the campus moved to its present site &mdash; a date still marked jointly by alumni associations and the university administration each year.</p>
            
            <p>Today it is the largest university in Pakistan: eight faculties, fifty-three departments, and twenty research institutes and centres, serving an enrolment of more than 41,000 students under the guidance of over 700 faculty members.</p>
        </div>
        <div class="history_right">
            <div class="history_quote_box">
                <p class="quote_text">"For its first two years, the University of Karachi taught no one &mdash; it only examined the affiliated colleges of Sindh, before enrolling a single class of its own in 1953."</p>
                <p class="quote_author">From the university's founding years, 1951-1953</p>
            </div>
        </div>
    </div>
    <!-- End Our History Section -->

    <!-- New Academics Section -->
    <div class="academics_section">
        <div class="academics_intro">
            <div class="section_label">ACADEMICS</div>
            <h2>Eight faculties. Fifty-three departments.</h2>'''

content = content.replace(old_academics, new_academics)

with open('homepage.html', 'w', encoding='utf-8') as f:
    f.write(content)
