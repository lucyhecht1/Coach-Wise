function downloadPlayAsPDF(textContainerId, canvasId, pdfTitle, fileName) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Get the play content
    const playContent = document.getElementById(textContainerId).innerText;

    // Define PDF layout parameters
    const pageWidth = doc.internal.pageSize.width; // PDF page width
    const pageHeight = doc.internal.pageSize.height; // PDF page height
    const margin = 15; // Margin on all sides
    const contentWidth = pageWidth - margin * 2; // Width available for content
    let currentY = margin; // Current vertical position

    // Add Title
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.text(pdfTitle, margin, currentY);
    currentY += 10;

    // Add Play Content with Wrapping
    doc.setFont("times", "normal");
    doc.setFontSize(12);
    const wrappedText = doc.splitTextToSize(playContent, contentWidth);

    doc.text(wrappedText, margin, currentY);
    currentY += wrappedText.length * 6; // Adjust Y position based on text length

    // Check if there's enough room for the court image, or add a new page
    const courtCanvas = document.getElementById(canvasId);
    const courtHeight = courtCanvas
        ? (courtCanvas.height / courtCanvas.width) * contentWidth // Maintain aspect ratio
        : 0;
    const spaceNeeded = courtHeight + 20; // Image height + some padding

    if (currentY + spaceNeeded > pageHeight - margin) {
        doc.addPage(); // Add a new page if space is insufficient
        currentY = margin; // Reset Y position on new page
    }

    // Add Basketball Court Diagram
    if (courtCanvas) {
        const courtImage = courtCanvas.toDataURL("image/png");
        doc.addImage(courtImage, "PNG", margin, currentY, contentWidth, courtHeight);
        currentY += courtHeight + 10;
    } else {
        console.error("Court canvas not found.");
    }

    // Add Footer
    doc.setFont("courier", "italic");
    doc.setFontSize(10);
    doc.text(
        "Generated with CoachWise | Designed for Basketball Excellence",
        margin,
        pageHeight - margin
    );

    // Save the PDF
    doc.save(fileName);
}

// Event Listeners for Generate Play and Inbounds Play
document.getElementById("downloadPdfBtn")?.addEventListener("click", function () {
    downloadPlayAsPDF("generated_play_text", "courtCanvas", "Generated Basketball Play", "basketball_play.pdf");
});

document.getElementById("downloadInboundPdfBtn")?.addEventListener("click", function () {
    downloadPlayAsPDF("generated_inbound_play_text", "courtCanvasInbound", "Generated Inbounds Play", "inbound_play.pdf");
});
