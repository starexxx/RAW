document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/api/files");
    const data = await response.json();
    const tableBody = document.querySelector("#fileTable tbody");

    if (data.Starexx.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="2">No files found</td></tr>`;
        return;
    }

    data.Starexx.forEach((file, index) => {
        let fileName = Object.values(file)[0].split("/").pop();
        let row = document.createElement("tr");
        row.innerHTML = `<td>${index + 1}</td><td><a href="${Object.values(file)[0]}">${fileName}</a></td>`;
        tableBody.appendChild(row);
    });
});
