const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const fileButton = document.getElementById('fileButton');
const fileName = document.getElementById('fileName');
const boardType = document.getElementById('boardType');
const log = document.getElementById('log');

uploadForm.addEventListener('submit', handleSubmit, false);
fileButton.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) fileName.textContent = file.name;
});

function handleSubmit(e) {
    e.preventDefault();

    let filecontents;
    const file = fileInput.files[0];
    const reader = new FileReader();
    const board = boardType.value;

    reader.onload = function(event) {
        filecontents = event.target.result;

        let avrgirl = new AvrgirlArduino({
            board: board,
            debug: true
        });

        avrgirl.flash(filecontents, (error) =>  {
            if (error) {
                console.error(error);
            } else {
                console.info('done correctly.');
            }
        });

    };
    reader.readAsArrayBuffer(file);
}



