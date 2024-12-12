// Select all <div> elements with a class containing 'question-pnl'
const elements = document.querySelectorAll('div.question-pnl');

// Select the second <div> element (index 1 since it's 0-based)
const secondElement = elements[1];

if (secondElement) {
    // Select all <td> elements with a class containing 'bold' within the second <div>
    const boldTDs = secondElement.querySelectorAll('td.bold');

    // Check if there are at least 9 <td> elements with class 'bold'
    boldTDs.forEach((td, index) => {
        console.log(`Content of <td> with class 'bold' at index ${index}:`, td.textContent);
    });

    // Select all <td> elements with a class containing 'rightAns' within the second <div>
    const rightAnsTDs = secondElement.querySelectorAll('td.rightAns');

    // Print the first character of each matching <td> element with class 'rightAns'
    if (rightAnsTDs.length > 0) {
        console.log("\nFirst character of each <td> with class 'rightAns':");
        rightAnsTDs.forEach(td => {
            const firstChar = td.textContent.trim().charAt(0); // Trim to remove whitespace and get the first character
            console.log(firstChar);
        });
    } else {
        console.log("No <td> elements with class 'rightAns' found within the second <div>.");
    }
} else {
    console.log("Second <div> element not found.");
}


// Select all <div> elements with a class containing 'section-lbl'
const sectionElements = document.querySelectorAll('div.section-lbl span.bold');

// Print the content of all elements with their index
sectionElements.forEach((element, index) => {
    console.log(`Content of element at index ${index}:`, element.textContent);
});