document.getElementById('sel-img').addEventListener('click', function() {
    // Создаем элемент input для выбора файла
    let input = document.createElement('input');
    input.type = 'file';
    input.accept = '.png, .jpg, .jpeg, .webp, .ico, .svg';

    input.onchange = function(event) {
        // Получаем выбранный файл
        let file = event.target.files[0];
        if (file) {
            // Проверяем размер файла и тип
            let fileSize = file.size;
            let fileExtension = file.name.split('.').pop().toLowerCase();

            // Создаем URL для отображения картинки
            let reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('image').src = e.target.result;
            };
            reader.readAsDataURL(file);

            // Обновляем информацию о файле
            document.getElementById('img-size-info').textContent = (fileSize / 1024).toFixed(2) + ' KB';
            document.getElementById('img-extension-info').textContent = fileExtension;
        }
    };

    // Инициируем клик по input
    input.click();
});

document.getElementById('send-file').addEventListener('click', async function() {
    const imageElementSrc = document.getElementById('image').src;
    const imgTitle = document.getElementById('img-title').value;
    const imgDescription = document.getElementById('img-discription').value;
    const imgTags = document.getElementById('img-tags').value;
    const imgExtension = document.getElementById('img-extension-info').textContent;
    const imgSize = document.getElementById('img-size-info').textContent;

    if (imageElementSrc.indexOf('/img/empty.png') !== -1) {
        alert("Пожалуйста, выберите изображение.");
        return;
    }

    try {
        // Получаем данные изображения в формате Base64
        const base64 = imageElementSrc;

        // Создаем JSON объект с информацией об изображении
        const jsonData = {
            extension: imgExtension,
            size: imgSize,
            description: imgDescription,
            title: imgTitle,
            tags: imgTags,
            base64: base64
        };

        // Отправляем чанки на сервер
        await sendResponse(jsonData);

    } catch (error) {
        if(error.status){
            document.getElementById('response-status').textContent = error.status;
            document.getElementById('response-message').textContent = error.message;
            return;
        }
        
        // Обрабатываем ошибки
        document.getElementById('response-status').textContent = "Ошибка";
        document.getElementById('response-message').textContent = error.message;
    }
});

async function sendResponse(data) {
    document.getElementById('response-status').textContent = "Ожидание";
    document.getElementById('response-message').textContent = "Ожидание";

    const response = await fetch('/image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if(!response.ok){
        const error = new Error(response.statusText);
        error.status = response.status;
        throw error;
    }
 
    document.getElementById('response-status').textContent = response.status;
    document.getElementById('response-message').textContent = response.statusText;
}

