/* ==========================================================================
   Friends & Co — site chrome injector
   Single source of truth for the header, nav and footer across every mockup.

   Usage in a page:
     <body data-page="home">                     <!-- marks the active nav item -->
       <div data-chrome="header"></div>
       <main> ... page content ... </main>
       <div data-chrome="footer"></div>
       <script src="assets/js/chrome.js"></script>

   Markup and labels mirror the live Elementor header/footer exactly, including
   sentence-case navigation labels ("Free programs", not "Free Programs").
   Program names stay capitalised because they are proper nouns.

   Delivered as JS rather than fetched HTML partials so the mockups work both
   on GitHub Pages and when opened directly from disk (fetch() is blocked on
   file:// but <script src> is not).
   ========================================================================== */
(function () {
  'use strict';

  /* --- icons ------------------------------------------------------------- */
  var svg = function (vb, d, cls) {
    return '<svg viewBox="' + vb + '"' + (cls ? ' class="' + cls + '"' : '') +
           ' aria-hidden="true"><path d="' + d + '"/></svg>';
  };

  var ICON = {
    caret: svg('0 0 320 512', 'M31.3 192h257.3c17.8 0 26.7 21.5 14.1 34.1L174.1 354.8c-7.8 7.8-20.5 7.8-28.3 0L17.2 226.1C4.6 213.5 13.5 192 31.3 192z', 'caret'),
    chevron: svg('0 0 320 512', 'M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z'),
    heart: svg('0 0 576 512', 'M275.3 250.5c7 7.4 18.4 7.4 25.5 0l108.9-114.2c31.6-33.2 29.8-88.2-5.6-118.8-30.8-26.7-76.7-21.9-104.9 7.7L288 36.9l-11.1-11.6C248.7-4.4 202.8-9.2 172 17.5c-35.3 30.6-37.2 85.6-5.6 118.8l108.9 114.2zm290 77.6c-11.8-10.7-30.2-10-42.6 0L430.3 402c-11.3 9.1-25.4 14-40 14H272c-8.8 0-16-7.2-16-16s7.2-16 16-16h78.3c15.9 0 30.7-10.9 33.3-26.6 3.3-20-12.1-37.4-31.6-37.4H192c-27 0-53.1 9.3-74.1 26.3L71.4 384H16c-8.8 0-16 7.2-16 16v96c0 8.8 7.2 16 16 16h356.8c14.5 0 28.6-4.9 40-14L564 377c15.2-12.1 16.4-35.3 1.3-48.9z'),
    search: svg('0 0 512 512', 'M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z'),
    bars: svg('0 0 448 512', 'M16 132h416c8.837 0 16-7.163 16-16V76c0-8.837-7.163-16-16-16H16C7.163 60 0 67.163 0 76v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16z'),
    pin: svg('0 0 384 512', 'M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z'),
    phone: svg('0 0 512 512', 'M497.39 361.8l-112-48a24 24 0 0 0-28 6.9l-49.6 60.6A370.66 370.66 0 0 1 130.6 204.11l60.6-49.6a23.94 23.94 0 0 0 6.9-28l-48-112A24.16 24.16 0 0 0 122.6.61l-104 24A24 24 0 0 0 0 48c0 256.5 207.9 464 464 464a24 24 0 0 0 23.4-18.6l24-104a24.29 24.29 0 0 0-14.01-27.6z'),
    fax: svg('0 0 512 512', 'M480 160V77.25a32 32 0 0 0-9.38-22.63L425.37 9.37A32 32 0 0 0 402.75 0H160a32 32 0 0 0-32 32v448a32 32 0 0 0 32 32h320a32 32 0 0 0 32-32V192a32 32 0 0 0-32-32zM288 432a16 16 0 0 1-16 16h-32a16 16 0 0 1-16-16v-32a16 16 0 0 1 16-16h32a16 16 0 0 1 16 16zm0-128a16 16 0 0 1-16 16h-32a16 16 0 0 1-16-16v-32a16 16 0 0 1 16-16h32a16 16 0 0 1 16 16zm128 128a16 16 0 0 1-16 16h-32a16 16 0 0 1-16-16v-32a16 16 0 0 1 16-16h32a16 16 0 0 1 16 16zm0-128a16 16 0 0 1-16 16h-32a16 16 0 0 1-16-16v-32a16 16 0 0 1 16-16h32a16 16 0 0 1 16 16zm0-112H192V64h160v48a16 16 0 0 0 16 16h48zM64 128H32a32 32 0 0 0-32 32v320a32 32 0 0 0 32 32h32a32 32 0 0 0 32-32V160a32 32 0 0 0-32-32z'),
    mail: svg('0 0 512 512', 'M464 64H48C21.49 64 0 85.49 0 112v288c0 26.51 21.49 48 48 48h416c26.51 0 48-21.49 48-48V112c0-26.51-21.49-48-48-48zm0 48v40.805c-22.422 18.259-58.168 46.651-134.587 106.49-16.841 13.247-50.201 45.072-73.413 44.701-23.208.375-56.579-31.459-73.413-44.701C106.18 199.465 70.425 171.067 48 152.805V112h416zM48 400V214.398c22.914 18.251 55.409 43.862 104.938 82.646 21.857 17.205 60.134 55.186 103.062 54.955 42.717.231 80.509-37.199 103.053-54.947 49.528-38.783 82.032-64.401 104.947-82.653V400H48z'),
    facebook: svg('0 0 512 512', 'M504 256C504 119 393 8 256 8S8 119 8 256c0 123.78 90.69 226.38 209.25 245V327.69h-63V256h63v-54.64c0-62.15 37-96.48 93.67-96.48 27.14 0 55.52 4.84 55.52 4.84v61h-31.28c-30.8 0-40.41 19.12-40.41 38.73V256h68.78l-11 71.69h-57.78V501C413.31 482.38 504 379.78 504 256z'),
    youtube: svg('0 0 576 512', 'M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.78 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z'),
    linkedin: svg('0 0 448 512', 'M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3c0-17.8-14.4-32.3-32-32.3zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z'),
    instagram: svg('0 0 448 512', 'M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z')
  };

  /* --- link map -----------------------------------------------------------
     Every internal link points at a local mockup file. Nothing links back to
     friendsco.org — the whole point of the mockup is that Paul can click
     through it without landing on the live WordPress site.

     Pages that don't exist in the mockup set yet resolve to '#'. They are
     listed in TODO below so it stays obvious which ones are stubs.
     -------------------------------------------------------------------------- */
  var P = {
    home:        'index.html',
    programs:    'friendship-services.html',
    visiting:    'visiting-companions.html',
    lets:        'lets-do-events.html',
    spanish:     'spanish-language-programs.html',
    coffee:      'coffee-talk.html',
    phone:       'phone-companions.html',
    cards:       'cards-connect.html',
    events:      'events.html',
    volunteer:   'get-involved.html',
    refer:       'refer.html',
    about:       'about.html',
    reports:     'annual-reports.html',
    team:        'staff-and-board.html',
    news:        'news.html',
    contact:     'contact.html',
    support:     'support-friends-co.html',
    donate:      'donate.html',
    planned:     'planned-giving.html',
    corporate:   'corporate-sponsorship.html',
    other:       'other-ways-to-give.html',
    memorials:   'remembering-our-friends.html',
    join:        'join.html',
    apply:       'volunteer-apply.html',
    search:      'search-results.html',
    portal:      'volunteer-portal.html',
    matchhub:    'visiting-companions-match.html'
  };

  /* Not yet built as mockups — deliberately dead so they are visible as gaps
     rather than silently bouncing to WordPress. */
  var TODO = '#';

  /* --- primary navigation ------------------------------------------------
     `key` matches <body data-page="..."> to set the active state.
     Labels are sentence case, matching the live site.
     ---------------------------------------------------------------------- */
  var NAV = [
    {
      key: 'programs', label: 'Free programs', href: P.programs,
      children: [
        { label: 'Start here', href: P.programs },
        {
          label: 'Meet in person', href: P.programs,
          children: [
            { label: 'One-on-one visiting companions', href: P.visiting },
            { label: 'Let’s do coffee / Let’s do lunch café 🏳️‍🌈', href: P.lets },
            { label: 'Conexiones comunitarias (Español)', href: P.spanish }
          ]
        },
        {
          label: 'Talk on the phone', href: P.coffee,
          children: [
            { label: 'Tue & Thurs coffee talk calls', href: P.coffee },
            { label: 'Weekly 1-on-1 phone friends', href: P.phone }
          ]
        },
        { label: 'Receive friendly mail', href: P.cards },
        { label: 'Events calendar', href: P.events },
        {
          label: 'See all programs', href: P.programs,
          children: [
            { label: 'Cards Connect', href: P.cards },
            { label: 'Coffee Talk', href: P.coffee },
            { label: 'Conexiones Comunitarias', href: P.spanish },
            { label: 'Let’s Do Coffee / Let’s Do Lunch Café', href: P.lets },
            { label: 'Phone Companions', href: P.phone },
            { label: 'Visiting Companions', href: P.visiting }
          ]
        }
      ]
    },
    {
      key: 'volunteer', label: 'Volunteer', href: P.volunteer,
      children: [
        { label: 'Volunteer opportunities', href: P.volunteer },
        { label: 'Apply to volunteer', href: P.apply },
        { label: 'Matching hub', href: P.matchhub },
        { label: 'Volunteer portal', href: P.portal }
      ]
    },
    {
      key: 'about', label: 'About', href: P.about,
      children: [
        { label: 'About us', href: P.about },
        { label: 'Annual reports', href: P.reports },
        { label: 'Our team', href: P.team },
        { label: 'Latest news', href: P.news },
        { label: 'Contact', href: P.contact }
      ]
    },
    {
      key: 'support', label: 'Support', href: P.support,
      children: [
        { label: 'Give today', href: P.donate },
        { label: 'Planned giving', href: P.planned },
        { label: 'Corporate sponsorship', href: P.corporate },
        { label: 'Other ways to give', href: P.other }
      ]
    },
    { key: 'home', label: 'Home', href: P.home }
  ];

  function renderSub(items) {
    return '<ul class="sub">' + items.map(function (it) {
      var inner = it.children
        ? '<a href="' + it.href + '">' + it.label + ICON.caret + '</a>' + renderSub(it.children)
        : '<a href="' + it.href + '">' + it.label + '</a>';
      return '<li>' + inner + '</li>';
    }).join('') + '</ul>';
  }

  function renderNav(active) {
    return NAV.map(function (top) {
      var cls = (top.key === active) ? ' class="active"' : '';
      var caret = top.children ? ' ' + ICON.caret : '';
      return '<li' + cls + '><a href="' + top.href + '">' + top.label + caret + '</a>' +
             (top.children ? renderSub(top.children) : '') + '</li>';
    }).join('');
  }

  /* --- header ------------------------------------------------------------ */
  function headerHTML(active) {
    return '' +
    '<header class="site-header">' +
      '<a class="logo" href="' + P.home + '">' +
        '<img src="assets/img/site-logo-350x100.png" alt="Friends &amp; Co">' +
      '</a>' +
      '<nav class="main-nav" aria-label="Main menu"><ul>' + renderNav(active) + '</ul></nav>' +
      '<div class="header-actions">' +
        '<a class="btn-give" href="' + P.donate + '">' + ICON.heart + '<span>Give</span></a>' +
        '<button class="btn-search" type="button" aria-label="Search">' + ICON.search + '</button>' +
        '<button class="btn-hamburger" type="button" aria-label="Menu" aria-expanded="false" data-menu-toggle>' + ICON.bars + '</button>' +
      '</div>' +
    '</header>' +
    '<nav class="mobile-menu" id="mobileMenu" aria-label="Mobile menu"><ul>' +
      NAV.map(function (t) { return '<li><a href="' + t.href + '">' + t.label + '</a></li>'; }).join('') +
      '<li><a class="menu-give" href="' + P.donate + '">Give</a></li>' +
    '</ul></nav>';
  }

  /* --- footer ------------------------------------------------------------ */
  var FOOTER_PROGRAMS = [
    ['Cards Connect', P.cards],
    ['Coffee Talk', P.coffee],
    ['Conexiones Comunitarias', P.spanish],
    ['Let’s Do Lunch Cafe &amp; Let’s Do Coffee', P.lets],
    ['Phone Companions', P.phone],
    ['Visiting Companions', P.visiting]
  ];

  var FOOTER_INVOLVED = [
    ['Become a volunteer', P.volunteer],
    ['Refer an older adult', P.refer],
    ['Current volunteers portal', P.portal],
    ['Board &amp; staff', P.team],
    ['Contact us', P.contact]
  ];

  function linkList(rows) {
    return '<ul class="footer-links">' + rows.map(function (r) {
      return '<li><a href="' + r[1] + '">' + ICON.chevron + '<span>' + r[0] + '</span></a></li>';
    }).join('') + '</ul>';
  }

  function footerHTML(assetPath) {
    var img = assetPath || 'assets/img/';
    return '' +
    '<footer class="site-footer">' +
      '<div class="footer-newsletter"><div class="inner">' +
        '<div><h3>Stay in the loop</h3><p>Get monthly updates and news from Friends &amp; Co.</p></div>' +
        '<form class="newsletter-form" onsubmit="return false;">' +
          '<label class="nf-label"><span>* Email</span><input type="email" name="email" required></label>' +
          '<label class="nf-label"><span>* First Name</span><input type="text" name="fname" required></label>' +
          '<label class="nf-label"><span>Last Name</span><input type="text" name="lname"></label>' +
          '<button type="submit">YES, SIGN ME UP!</button>' +
        '</form>' +
      '</div></div>' +

      '<div class="footer-main"><div class="inner">' +
        '<div>' +
          '<img class="footer-logo" src="assets/img/friends-co-logo-white.png" alt="Friends &amp; Co">' +
          '<ul class="contact-list">' +
            '<li>' + ICON.pin + '<span>2550 University Avenue W.<br>Suite 260-S<br>St. Paul, MN 55114<br>*Please note that Hwy 280 is closed for construction.</span></li>' +
            '<li>' + ICON.phone + '<a href="tel:+16127211400">Phone: 612-721-1400</a></li>' +
            '<li>' + ICON.fax + '<span>Fax: 612-721-5848</span></li>' +
            '<li>' + ICON.mail + '<a href="mailto:info@friendsco.org">Email: info@friendsco.org</a></li>' +
          '</ul>' +
        '</div>' +

        '<div><h4>Free programs</h4>' + linkList(FOOTER_PROGRAMS) + '</div>' +
        '<div><h4>Get involved</h4>' + linkList(FOOTER_INVOLVED) + '</div>' +

        '<div>' +
          '<h4>Support our mission</h4>' +
          '<div class="footer-give"><a class="btn-give" href="' + P.donate + '">' + ICON.heart + '<span>Give</span></a></div>' +
          '<div class="footer-badges">' +
            '<a href="https://www.charitynavigator.org/ein/410986200" target="_blank" rel="noopener"><img src="' + img + 'charity-navigator-logo.png" alt="Charity Navigator four-star charity"></a>' +
            '<a href="https://smartgivers.org/organizations/friends-co/" target="_blank" rel="noopener"><img src="' + img + 'charities-review-council-logo.png" alt="Charities Review Council — meets standards"></a>' +
          '</div>' +
          '<div class="footer-social">' +
            '<a href="https://www.facebook.com/FriendsCoMN/" target="_blank" rel="noopener" aria-label="Facebook">' + ICON.facebook + '</a>' +
            '<a href="https://www.youtube.com/channel/UCR9Hg7v8qScNMrSpesiZx0Q" target="_blank" rel="noopener" aria-label="YouTube">' + ICON.youtube + '</a>' +
            '<a href="https://www.linkedin.com/company/friendscomn/" target="_blank" rel="noopener" aria-label="LinkedIn">' + ICON.linkedin + '</a>' +
            '<a href="https://www.instagram.com/friendscomn" target="_blank" rel="noopener" aria-label="Instagram">' + ICON.instagram + '</a>' +
          '</div>' +
        '</div>' +
      '</div></div>' +

      '<div class="footer-bottom">' +
        '<p>Friends &amp; Co formerly Little Brothers – Friends of the Elderly Twin Cities, EIN 41-0986200, previous address 1845 E. Lake St, Minneapolis, MN</p>' +
        '<p>&copy; ' + new Date().getFullYear() + ' Friends &amp; Co. All rights reserved. | Privacy policy</p>' +
      '</div>' +
    '</footer>';
  }

  /* --- mount -------------------------------------------------------------- */
  function mount() {
    var active = document.body.getAttribute('data-page') || '';
    var assetPath = document.body.getAttribute('data-assets') || 'assets/img/';

    var h = document.querySelector('[data-chrome="header"]');
    if (h) h.outerHTML = headerHTML(active);

    var f = document.querySelector('[data-chrome="footer"]');
    if (f) f.outerHTML = footerHTML(assetPath);

    var toggle = document.querySelector('[data-menu-toggle]');
    if (toggle) {
      toggle.addEventListener('click', function () {
        var m = document.getElementById('mobileMenu');
        m.classList.toggle('open');
        toggle.setAttribute('aria-expanded', m.classList.contains('open'));
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
