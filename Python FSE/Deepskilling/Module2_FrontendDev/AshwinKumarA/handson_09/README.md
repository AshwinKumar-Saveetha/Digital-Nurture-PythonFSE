# Hands-On 09 -- Accessibility and Cross-Browser Compatibility

## Student Details

**Student Name:** Ashwin Kumar A\
**Track:** Python Full Stack Engineer\
**Program:** Cognizant Digital Nurture 5.0

## Project Overview

This project was completed as part of **Cognizant Digital Nurture 5.0 --
Module 2: Frontend Development (Hands-On 09)**.

The objective was to improve the accessibility, keyboard usability,
colour contrast and browser compatibility of the existing **Student
Portal** application while following WCAG accessibility guidelines and
frontend best practices.

------------------------------------------------------------------------

# Features Implemented

## Task 1 -- Accessibility Audit

-   Initial Accessibility Score: **87**
-   Fixed heading hierarchy.
-   Added accessible labels.
-   Improved semantic HTML.
-   Corrected button accessibility.
-   Final Accessibility Score: **100**

### Screenshot

**Initial Accessibility Audit**

![Initial Accessibility
Audit](images/task1_01_initial_accessibility_audit.png)

**Improved Accessibility Audit**

![Improved Accessibility
Audit](images/task1_02_improved_accessibility_audit.png)

------------------------------------------------------------------------

## Task 2 -- ARIA and Keyboard Navigation

-   Added `aria-label`, `aria-current`, `aria-live`, `role="status"` and
    `aria-expanded`.
-   Enabled keyboard navigation for course cards.
-   Added Enter-key activation.
-   Verified keyboard-only navigation.

### Screenshot

**Keyboard Navigation**

![Keyboard Navigation](images/task2_01_keyboard_navigation.png)

------------------------------------------------------------------------

## Task 3 -- Colour Contrast and Browser Compatibility

### Colour Theme

-   Primary Colour: **#bfd42f**
-   Primary Text: **#1f2a00**
-   WCAG AA compliant contrast.

### Browser Compatibility

-   CSS Grid support verified using Can I Use.
-   CSS feature detection implemented.
-   Flexbox fallback added.
-   css-vars-ponyfill integrated.
-   Cross-browser testing completed.

### Screenshots

**Colour Contrast**

![Colour Contrast](images/task3_01_colour_contrast_check.png)

**CSS Grid Browser Support**

![CSS Grid Browser
Support](images/task3_02_css_grid_browser_support.png)

**Cross Browser Testing**

![Cross Browser Testing](images/task3_03_cross_browser_testing.png)

**Final Accessibility Audit**

![Final Accessibility
Audit](images/task3_04_final_accessibility_audit.png)

------------------------------------------------------------------------

# Folder Structure

``` text
handson_09
├── images/
├── index.html
├── styles.css
├── app.js
├── data.js
└── README.md
```

------------------------------------------------------------------------


# Application Flow

1.  Student Portal loads.
2.  Student statistics are displayed.
3.  Courses load dynamically.
4.  Search and sort features work.
5.  Notifications are loaded.
6.  Keyboard navigation is supported.

------------------------------------------------------------------------

# Validation

-   Lighthouse Accessibility Audit
-   Keyboard Navigation
-   ARIA Validation
-   Colour Contrast Verification
-   Browser Compatibility
-   Responsive Layout

------------------------------------------------------------------------


# Conclusion

The Student Portal was enhanced with semantic HTML, ARIA attributes,
keyboard accessibility, improved colour contrast, browser compatibility
verification and responsive design. The project successfully achieved a
**100/100 Lighthouse Accessibility Score**.
