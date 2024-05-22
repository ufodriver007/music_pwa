const DEBUG = false;
let DOMAIN = "";
let VK_APP_ID = 0;
if (DEBUG) {
    DOMAIN = "http://127.0.0.1:8000";
    VK_APP_ID = 0;
} else {
    DOMAIN = "https://www.mint-coast.ru";
    VK_APP_ID = 51913447;
}
const GENERAL_ENDPOINT = DOMAIN + "/api/v1";
const VK_REDIRECT_URL = DOMAIN + "/complete/vk";


function setHeight() {
    const songList = document.getElementById("song-list");
    const searchList = document.getElementById("search-list");
    const footer = document.querySelector(".footer");

    const footerTop = footer.offsetTop;
    const songListTop = songList.offsetTop;
    const searchListTop = searchList.offsetTop;

    const songListHeight = footerTop - songListTop;
    const searchListHeight = footerTop - searchListTop;
    songList.style.height = songListHeight + "px";
    searchList.style.height = searchListHeight + "px";
}

// Вызываем функцию при загрузке страницы и изменении размеров окна
window.addEventListener("load", setHeight);
window.addEventListener("resize", setHeight);

let sw = false;
let orig_width;

function switchSearchList() {
    if (sw === false) {
        const searchList = document.querySelector(".search-list");
        const playlist = document.getElementById("playlist");

        searchList.style.display = "none";
        orig_width = playlist.style.width;
        playlist.style.width = "100%";
        sw = true;
        setHeight();
    } else {
        const searchList = document.querySelector(".search-list");
        const playlist = document.getElementById("playlist");

        searchList.style.display = "block";
        playlist.style.width = orig_width;
        sw = false;
    }
}

let ud_sw = false;
const pl_buttons = document.querySelector(".pl-buttons");
const switcher = document.querySelector(".switcher");
switcher.addEventListener("click", switchSearchList);

function buttons_visible_switch() {
    if (ud_sw == false) {
        pl_buttons.style.display = "none";
        ud_sw = true;
    } else {
        pl_buttons.style.display = "block";
        ud_sw = false;
    }
    setHeight();
}

const ud_switcher = document.querySelector(".btn-h");
ud_switcher.addEventListener("click", buttons_visible_switch);

// объект пользователя
let user = {
    username: "test_admin",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
};

// токен авторизации
let userToken = "asdfg12345";

// объект песни, воспроизводимой в данный момент
let currentSong = {};

// список всех плейлистов пользователя
let allPlaylists = [];

// объект плейлиста
let playList = {
    id: 2,
    songs: [
        {
            id: 75,
            name: "Mann gegen Mann",
            author: "Rammstein",
            album: "Rosenrot",
            bitrate: "327",
            duration_text: "03:50",
            duration: "230",
            album_cover_url:
                "https://content-3.foto.my.mail.ru/community/artist_rammstein/_musicplaylistcover/i-280.jpg",
            url: "https://moosic.my.mail.ru/file/43aa710652c1ca9e967a5bcdd804961d.mp3",
        },
        {
            id: 77,
            name: "Rammstein - Keine Lust.mp3",
            author: "Rammstein",
            album: "Mein Teil",
            bitrate: "192",
            duration_text: "03:43",
            duration: "223",
            album_cover_url: null,
            url: "https://moosic.my.mail.ru/file/dbe5cf13286749ef0ca8029243d90157.mp3",
        },
    ],
    name: "My_test_playlist",
    user: 1,
};

// список песен(объектов) в поисковике
let search_results = [];

// инициализация элементов страницы
const page_title = document.querySelector("title");
const h_username = document.getElementById("username");
const song_title = document.getElementById("main-song-title");
const playlist_title = document.getElementById("playlist-title");
const player = document.getElementById("player");
const search_input = document.getElementById("search-input");
search_input.addEventListener('input', function (event) {
    // Очищаем список предположений для предиктивного ввода
    datalist.innerHTML = '';

    db.requests.each(req => {
        if (req.request.toLowerCase().startsWith(event.target.value.toLowerCase())) {
            // Проверяем количество опций в datalist
            if (datalist.options.length < 6) {
                const newOption = document.createElement('option');
                newOption.value = req.request;
                datalist.appendChild(newOption);
            }
        }
    })
});
const datalist = document.getElementById("suggestions");
const search_button = document.getElementById("search-button");
const shuffle_button = document.getElementById("btn-shuffle");

const login_input = document.getElementById("login-input");
const password_input = document.getElementById("password-input");
const login_button = document.getElementById("login-button");
const login_screen = document.querySelector(".login-screen");
const logout_button = document.getElementById("logout-button");
const settings_button = document.getElementById("settings-button");

const pl_table = document.querySelector(".pl-table");
const result_table = document.getElementById("result_table");

async function render_vk_button() {
    //Отрисовка кнопки VK
    const VKID = window.VKIDSDK;
    VKID.Config.set({
      app: VK_APP_ID, // Идентификатор приложения.
      redirectUrl: VK_REDIRECT_URL, // Адрес для перехода после авторизации.
      // state: 'dj29fnsadjsd82...' // Произвольная строка состояния приложения.
    });
    // Создание экземпляра кнопки.
    const oneTap = new VKID.OneTap();
    // Получение контейнера из разметки.
    const container = document.getElementById('VkIdSdkOneTap');
    // Проверка наличия кнопки в разметке.
    if (container) {
        container.innerHTML = '';
      // Отрисовка кнопки в контейнере с именем приложения APP_NAME, светлой темой и на русском языке.
      oneTap.render({ container: container, scheme: VKID.Scheme.DARK, lang: VKID.Languages.RUS, showAlternativeLogin: true });
    }
}

render_vk_button();

//login
async function login() {
    user.username = login_input.value;
    user.password = password_input.value;

    login_input.value = '';
    password_input.value = '';

    try {
        let response = await fetch(DOMAIN + "/auth/token/login", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json;charset=utf-8",
            },
            body: JSON.stringify(user),
        });
        if (response.ok) {
            let answer = await response.json(); // Получить JSON ответ от сервера
            userToken = answer.auth_token;
            login_screen.style.cssText = "display:none !important";
            h_username.innerHTML = user.username.replace(/\d/g, '');  // удалем из username цифры, т.к. социальные аккаунты имеют username типа Маша402834234892

            // устанавливаем куку на 1 год
            setCookie("auth_token", userToken, {expires: new Date(new Date().setFullYear(new Date().getFullYear() + 1))});
            // получаем user.id
            await check_logged();
            // сохраняем id, username, плейлисты в локальную БД
            await save_user_info();
        } else {
            userToken = null;
            alert("Wrong data!");
        }
    } catch (err) {
        alert("NetworkError");
    }
}

login_button.addEventListener("click", login);

//logout
async function logout() {
    //logout по токену
    let response = await fetch(DOMAIN + "/auth/token/logout", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json;charset=utf-8",
            Authorization: "Token " + getCookie("auth_token"),
        }
    });

    user = {};
    userToken = "";
    login_screen.style.cssText = "display:block !important";
    setCookie("auth_token", "");
    player.setAttribute("src", "");
    player.pause();

    await delete_user_info();
    await render_vk_button();
}

logout_button.addEventListener("click", logout);

const save_button = document.getElementById("save-button");
const save_music_button = document.getElementById("save-music-button");
const save_pl_music_button = document.getElementById("save-pl-music-button");
const save_song_music_button = document.getElementById("save-song-music-button");
const save_music_checkbox = document.getElementById("ch-save-music-files");
save_music_checkbox.addEventListener("change", save_user_info);
const delete_music_button = document.getElementById("del-music-button");
const audioElement = document.querySelector("audio");
const t_size = document.getElementById("t-size");

async function show_settings() {
    const settingsModal = new bootstrap.Modal("#settingsModal");
    settingsModal.show();

    // получаем из indexeddb значение галочки "Сохранять локально при добавлении в плейлист"
    const usr = await db.user.where('username').equals(user.username).first();
    if (usr) {
        if (usr.savelocal) {
            save_music_checkbox.checked = true;
        }
    }

    // получение общего размера локальной БД
    get_db_size()
        .then(result => {
            t_size.textContent = "Общий размер локальной базы данных: " + result + "Мб"
        })
}

settings_button.addEventListener("click", show_settings);

// проверка, что в куках есть токен авторизации, логин и получение user.id
async function check_logged() {
    try {
        // добавление к запросу рандомных параметров, чтобы запрос не кешировался браузером
        let response = await fetch(GENERAL_ENDPOINT + "/auth/users/me/?_=" + Math.random(), {
            method: "GET",
            headers: {
                Accept: "application/json",
                Authorization: "Token " + getCookie("auth_token"),
            },
        });
        let json_data = await response.json();
        if (response.ok) {
            user.id = json_data.id;
            user.username = json_data.username;

            login_screen.style.cssText = "display:none !important";
            h_username.innerHTML = user.username.replace(/\d/g, '');  // удалем из username цифры, т.к. социальные аккаунты имеют username типа Маша402834234892

            await load_playlists();
            if (allPlaylists.length > 0) {
                await draw_playlist(allPlaylists[0]);
            } else  {
                alert("У Вас нет плейлистов. Вы можете создать плейлист, нажав кнопку '+'");
            }
        } else {
            console.log("Не залогинен");
        }
    } catch (err) {
        // если нет соединения, проверим что есть userToken в куках и id,
        //   username и плейлисты в локальной БД
        console.log("Сервер недоступен " + err);
        try {
            userToken = getCookie("auth_token");
            local_user = await db.user.orderBy("id").first();

            if (userToken && local_user) {
                console.log("Данные будут взяты из куки и локальной БД");
                user.id = local_user.id;
                user.username = local_user.username;

                login_screen.style.cssText = "display:none !important";
                h_username.innerHTML = user.username.replace(/\d/g, '');  // удалем из username цифры, т.к. социальные аккаунты имеют username типа Маша402834234892

                db.playlists.each(pl => {
                    allPlaylists.push(pl.playlist);
                })
                    .then(async () => {
                        if (allPlaylists.length > 0) {
                            await draw_playlist(allPlaylists[0]);
                        }
                    })
            } else {
                console.log("Пользователь не был залогинен");
            }
        } catch (err) {
            console.log(err);
        }
    }
}

if (login_input.value && password_input.value) {
    login();
} else {
    check_logged();
}

// Declare DB
var db = new Dexie("UserDatabase");
db.version(1).stores({
    playlists: "++id,playlist",
    user: "id,username,savelocal",
    files: '++id, name, data',
    requests: '++id, request'// Хранилище для файлов
});
var totalSize = 0;                   // размер всех файлов при загрузке save_all_music_files()
var totalIndexedDBSize = 0;          // общий размер локальной БД

async function rename_playlist() {
    // alert(playList.name);
    const renamePlaylistModal = new bootstrap.Modal("#rn-pl-modal");
    renamePlaylistModal.show();

    const rn_input = document.getElementById("rn-pl-name");
    const rn_pl_button = document.getElementById("rn-pl-button");

    rn_input.value = playList.name;
    rn_pl_button.addEventListener("click", async () => {
        try {
            playList.name = rn_input.value;
            let resp = await fetch(GENERAL_ENDPOINT + `/playlist/` + playList.id + "/", {
                method: "PUT",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json;charset=utf-8",
                    Authorization: "Token " + getCookie("auth_token"),
                },
                body: JSON.stringify(playList),
            });
            if (resp.ok) {
                let answer = await resp.json();      // Получить JSON ответ от сервера
                console.log("Playlist renamed " + answer.name);
                renamePlaylistModal.hide();
                await load_playlists();
                for (i of allPlaylists) {
                    console.log(i.name);
                    if (answer.name == i.name) {
                        playList = i;
                        await draw_playlist(playList);
                        break;
                    }
                }
                await save_user_info();
            }
        } catch (err) {
            alert("Сервер недоступен");
            console.log(err);
        }
    });
}

playlist_title.addEventListener("click", rename_playlist);

async function delete_user_info() {
    try {
        // Удаляем все плейлисты
        await db.playlists.clear();
        // Удаляем инфо пользователя
        await db.user.clear();
        //Удаляем историю запросов
        await db.requests.clear();
    } catch (err) {
        console.log(err);
    }
}

async function save_user_info() {
    // Добавляем все плейлисты из allPlaylists в БД
    await load_playlists();
    await delete_user_info();

    try {
        for (pl of allPlaylists) {
            await db.playlists.add({playlist: pl});
        }
        // Добавляем имя пользователя и его ID в БД
        await db.user.add({id: user.id, username: user.username, savelocal: save_music_checkbox.checked});
    } catch (err) {
        console.log(err);
    }
}

function get_db_size() {
    // логика рассчёта объёма БД
    return new Promise((resolve, reject) => {
        totalIndexedDBSize = 0;
        db.files.each(item => {
            totalIndexedDBSize += (item.content.size / 1024 / 1024); // Не вызывать здесь toFixed(), чтобы сохранить точность
        }).then(() => {
            resolve(totalIndexedDBSize.toFixed(1)); // Округление до 1 знака после запятой и передача результата в resolve
        }).catch(error => {
            reject(error);
        });
    });
}

async function play_song_from_bd(fileName) {
    try {
        const song = await db.files.where('name').equals(fileName).first(); // Ждем выполнения запроса и получаем объект песни

        if (song) {
            const blobUrl = URL.createObjectURL(song.content); // Создаем URL для Blob-объекта

            audioElement.src = blobUrl;
            audioElement.play();
        } else {
            console.error('Song not found in IndexedDB');
        }
    } catch (error) {
        console.error('Error retrieving song from IndexedDB:', error);
    }
}

async function save_music_file(url) {
    let file_name = url.split("/").pop();

    try {
        const response = await fetch(GENERAL_ENDPOINT + '/proxy/?url=' + url);

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const blob = await response.blob();
        const size = blob.size;
        totalSize += size;

        await db.files.add({name: file_name, content: blob});

        console.log("File " + file_name + " saved to IndexedDB");
        await draw_playlist(playList);
    } catch (error) {
        alert("Ошибка при сохранении файла");
        console.error('Error downloading file or saving to IndexedDB:', error);
    }
}

async function download_files_from_list(all_urls) {
    let urls = [];
    for (let url of all_urls) {
        const song_in_local_db = await db.files.where('name').equals(url.split('/').slice(-1)[0]).first();
        if (song_in_local_db === undefined) {
            urls.push(url);
        }
    }

    alert("Всего будет скачано " + urls.length + " файлов");
    totalSize = 0;

    const downloadPromises = urls.map(url => save_music_file(url));
    await Promise.all(downloadPromises);

    alert("Скачивание завершено. Размер всех скачанных файлов " + (Math.round(totalSize / 1024 / 1024)) + "Мб");
}

async function save_all_music_files() {
    save_music_button.classList.add("disabled");
    save_pl_music_button.classList.add("disabled");
    save_song_music_button.classList.add("disabled");
    await save_user_info();

    let all_urls = allPlaylists.flatMap(pl => pl.songs.map(song => song.url));
    await download_files_from_list(all_urls);
    await draw_playlist(playList);
    save_music_button.classList.remove("disabled");
    save_pl_music_button.classList.remove("disabled");
    save_song_music_button.classList.remove("disabled");
}
save_music_button.addEventListener("click", save_all_music_files);

async function save_current_playlist_music_files() {
    save_music_button.classList.add("disabled");
    save_pl_music_button.classList.add("disabled");
    save_song_music_button.classList.add("disabled");
    await save_user_info();

    let all_urls = playList.songs.flatMap(song => song.url);
    await download_files_from_list(all_urls);
    await draw_playlist(playList);
    save_music_button.classList.remove("disabled");
    save_pl_music_button.classList.remove("disabled");
    save_song_music_button.classList.remove("disabled");
}

save_pl_music_button.addEventListener("click", save_current_playlist_music_files);

async function save_current_song_file() {
    save_music_button.classList.add("disabled");
    save_pl_music_button.classList.add("disabled");
    save_song_music_button.classList.add("disabled");
    await save_user_info();

    if (Object.keys(currentSong).length === 0) {
        alert("Выберите песню для скачивания!");
    } else {
        if (playList.songs.includes(currentSong)) {
            await save_music_file(currentSong.url);
            alert(`Сохранён файл ${currentSong.name}`);
            await draw_playlist(playList);
        } else {
            alert("Сначала добавьте песню в плейлист");
        }
    }
    save_music_button.classList.remove("disabled");
    save_pl_music_button.classList.remove("disabled");
    save_song_music_button.classList.remove("disabled");
}
save_song_music_button.addEventListener("click", save_current_song_file);

async function delete_music_files() {
    if (confirm("Внимание! Вы удаляете все локальные файлы с музыкой!")) {
        // Удаляем файлы музыки из БД
        await db.files.clear();
        t_size.textContent = "Общий размер локальной базы данных: 0Мб"
        alert("Все локальные файлы с музыкой удалены");
        await draw_playlist(playList);
    } else {
        console.log("Удаление локальных файлов отменено пользователем");
    }
}

delete_music_button.addEventListener("click", delete_music_files);

async function load_playlists() {
    let response = await fetch(GENERAL_ENDPOINT + "/playlist/?user=" + user.id, {
        method: "GET",
        headers: {
            Accept: "application/json",
            Authorization: "Token " + getCookie("auth_token"),
        },
    });

    if (response.ok) {
        let json_data = await response.json();
        if (json_data.length > 0) {
            allPlaylists = json_data;
        } else {
            allPlaylists = [];
        }
    }
}

async function play_song() {
    if (this.id !== undefined) {
        // определение по id песня из плейлиста или нет
        if (this.id.startsWith("rs")) {
            // если песня из результатов поиска
            song_url = this.id.slice(8);
            //console.log(search_results);
            for (song in search_results) {
                if (search_results[song].url == song_url) {
                    player.setAttribute("src", search_results[song].url);
                    song_title.textContent = search_results[song].name;
                    page_title.textContent = search_results[song].name;
                    // Сделать td активным
                    var elements = document.querySelectorAll('.orange'); // выбираем все элементы с классом 'orange'
                    elements.forEach(function (element) {
                        element.classList.remove('orange');                // удаляем класс 'orange' у каждого элемента
                    });
                    this.parentNode.classList.add("orange");

                    currentSong = search_results[song];
                }
            }

        } else {
            // если песня из плейлиста
            song_id = this.id.slice(8);
            for (let song of playList.songs) {
                if (song.id == song_id) {
                    let file_name = song.url.split("/").pop();
                    const found_song = await db.files.where('name').equals(file_name).first();
                    page_title.textContent = song.name;

                    if (found_song !== undefined) {
                        // Песня была найдена в БД
                        console.log('Запись найдена в локальной БД: ', found_song.name);
                        await play_song_from_bd(file_name);

                    } else {
                        player.setAttribute("src", song.url);
                    }

                    song_title.textContent = song.name;
                    // Сделать td активным
                    var elements = document.querySelectorAll('.orange'); // выбираем все элементы с классом 'orange'
                    elements.forEach(function (element) {
                        element.classList.remove('orange');                // удаляем класс 'orange' у каждого элемента
                    });
                    this.parentNode.classList.add("orange");

                    currentSong = song;
                }
            }
        }
    } else {
        // если само переключается на следующий трек

        // Сделать td активным
        elements = document.querySelectorAll('.orange'); // выбираем все элементы с классом 'orange'
        elements.forEach(function (element) {
            element.classList.remove('orange');                // удаляем класс 'orange' у каждого элемента
        });
        let tds = document.querySelectorAll('#song-list>table>tr>td');
        for (let td of tds) {
            if (td.id.slice(8) == currentSong.id) {
                td.parentNode.classList.add("orange");
            }
        }

        song_title.textContent = currentSong.name;
        page_title.textContent = currentSong.name;

        let file_name = currentSong.url.split("/").pop();
        const found_song = await db.files.where('name').equals(file_name).first();

        if (found_song !== undefined) {
            // Песня была найдена в БД
            console.log('Запись найдена в локальной БД: ', found_song.name);
            await play_song_from_bd(file_name);
        } else {
            player.setAttribute("src", currentSong.url);
        }
    }
}

async function remove_song_from_playlist() {
    song_id = this.id.slice(11);

    try {
        // разрыв связи в БД между плейлистом и песней
        let rem_playlist_query = await fetch(
            GENERAL_ENDPOINT + `/song/${song_id}/remove/${playList.id}/`,
            {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json;charset=utf-8",
                    Authorization: "Token " + getCookie("auth_token"),
                },
                body: "",
            }
        );
        if (rem_playlist_query.ok) {
            console.log("Song removed from playlist");
            // удаление песни из БД
            let delete_song_query = await fetch(
                GENERAL_ENDPOINT + `/song/${song_id}/`,
                {
                    method: "DELETE",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json;charset=utf-8",
                        Authorization: "Token " + getCookie("auth_token"),
                    },
                    body: "",
                });
            if (delete_song_query.ok) {
                console.log("Song removed from DB");
            }
        } else {
            console.log("Error! Cant remove song from playlist");
            return;
        }
    } catch (err) {
        alert("Сервер недоступен");
        return;
    }

    technical_name = "";
    // удаление песни из локальной переменной с плейлистом и получение технического имени файла
    for (let i = 0; i < playList.songs.length; i++) {
        if (playList.songs[i].id == song_id) {
            technical_name = playList.songs[i].url.split("/").pop();  // 35a607e441b4ef45ea0fba4482feddc2.mp3

            playList.songs.splice(i, 1);
            break;
        }
    }

    // удаление из локальной БД
    try {
        await db.files
            .where("name").equals(technical_name)
            .delete();
    } catch (err) {
        console.log("Can't delete local file " + err);
    }


    // перерисовка плейлиста визуально
    await draw_playlist(playList);
}

async function draw_playlist(playlist_obj) {
    pl_table.innerHTML = "";

    playList = playlist_obj;
    playlist_title.innerText = playList.name;

    // цикл для отрисовки всех песен плейлиста
    for (song of playlist_obj.songs) {
        let new_tr = document.createElement("tr");
        pl_table.appendChild(new_tr);

        let new_song_title = document.createElement("td");
        new_tr.appendChild(new_song_title);

        new_song_title.id = `pl_song_${song.id}`;
        new_song_title.className = "pl-song-title";
        new_song_title.textContent = song.name;
        new_song_title.addEventListener("click", play_song);

        new_td_2 = document.createElement("td");
        new_tr.appendChild(new_td_2);
        new_td_2.className = "pl-song-artist";
        new_td_2.textContent = song.author ?? "";

        new_td_3 = document.createElement("td");
        new_tr.appendChild(new_td_3);
        new_td_3.className = "pl-song-duration_text";
        new_td_3.textContent = song.duration_text;

        let new_td_4 = document.createElement("td");
        new_tr.appendChild(new_td_4);

        let new_rem_button = document.createElement("input");
        // new_td_4.appendChild(new_rem_button);
        new_tr.appendChild(new_rem_button);

        new_rem_button.type = "button";
        new_rem_button.id = `remove_btn_${song.id}`;

        // проверяем есть ли песня в лок.бд
        const song_in_local_db = await db.files.where('name').equals(song.url.split('/').slice(-1)[0]).first();
        if (song_in_local_db !== undefined) {
            // если есть в IndexedDB, красим кнопку в зелёный цвет
            new_rem_button.className = "btn btn-success btn-sm rm-btn my-1";
        } else {
            new_rem_button.className = "btn btn-dark btn-sm rm-btn my-1";
        }
        new_rem_button.value = "-";
        new_rem_button.addEventListener("click", remove_song_from_playlist);
    }

    // делаем "активной" если песня сейчас играет
    if (Object.keys(currentSong).length !== 0) {
        let tds = document.querySelectorAll('#song-list>table>tr>td');
        for (let td of tds) {
            if (td.id.slice(8) == currentSong.id) {
                td.parentNode.classList.add("orange");
            }
        }
    }
}

async function reload_playlist(playlist_obj) {
    await load_playlists();
    for (item of allPlaylists) {
        if (item.id === playlist_obj.id) {
            playList = item;
            return;
        }
    }
    console.log("Cant reload playlist!");
}

async function shuffle_playlist() {
    let shuffled_songs = playList.songs.sort(() => Math.random() - 0.5);
    playList.songs = shuffled_songs;
    await draw_playlist(playList);
}

shuffle_button.addEventListener("click", shuffle_playlist);

async function next_track() {
    for (let i = 0; i < playList.songs.length; i++) {
        if (playList.songs[i] === currentSong && i < playList.songs.length - 1) {
            currentSong = playList.songs[i + 1];
            await play_song();
            break;
        }
    }
}

player.onended = async function () {
    await next_track();
};

player.onpause = async function () {
    song_title.style.webkitAnimationPlayState = 'paused';
};

player.onplay = async function () {
    song_title.style.webkitAnimationPlayState = 'running';
};

async function rename_song() {
    if (!playList.songs.includes(currentSong)) {
        return;
    }

    const renameSongModal = new bootstrap.Modal("#rn-song-modal");
    renameSongModal.show();

    const rn_song_input = document.getElementById("rn-song-name");
    const rn_song_button = document.getElementById("rn-song-button");
    rn_song_button.addEventListener("click", handleSongRename);

    rn_song_input.value = currentSong.name;

    async function handleSongRename() {
        rn_song_button.removeEventListener("click", handleSongRename);
        currentSong.name = rn_song_input.value;
        try {
            let resp = await fetch(GENERAL_ENDPOINT + `/song/${currentSong.id}/`, {
                method: "PUT",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json;charset=utf-8",
                    Authorization: "Token " + getCookie("auth_token"),
                },
                body: JSON.stringify(currentSong),
            });
            if (resp.ok) {
                let answer = await resp.json();      // Получить JSON ответ от сервера
                console.log("Song renamed " + answer.name);
                renameSongModal.hide();
                await load_playlists();
                for (i of allPlaylists) {
                    if (playList.name == i.name) {
                        playList = i;
                        await draw_playlist(playList);
                        break;
                    }
                }
                currentSong = answer;
                song_title.textContent = currentSong.name;
            }
        } catch (err) {
            alert("Сервер недоступен");
            console.log(err);
        }
    }

    rn_song_button.addEventListener("click", handleSongRename);
}

song_title.addEventListener("click", rename_song);

async function add_song_to_playlist() {
    if (allPlaylists.length == 0) {
        alert("Некуда добавлять! Создайте плейлист.");
        return;
    }
    // находим объект песни в результатах по url, содеожащимуся в id кнопки
    let song = {};
    for (item in search_results) {
        if (search_results[item].url === this.id.slice(8)) {
            // создаём поверхностную копию
            song = {...search_results[item]};
            song.url = song.url.split('?')[0];
        }
    }

    try {
        // добавление песни в БД
        let resp = await fetch(GENERAL_ENDPOINT + "/song/", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json;charset=utf-8",
            },
            body: JSON.stringify(song),
        });
        if (resp.ok) {
            let answer = await resp.json(); // Получить JSON ответ от сервера
            console.log(answer.name + " added to DataBase!");

            // создание связи между песней и плейлистом
            let add_playlist_query = await fetch(
                GENERAL_ENDPOINT + `/song/${answer.id}/add/${playList.id}/`,
                {
                    method: "POST",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: "",
                }
            );
            if (add_playlist_query.ok) {
                console.log(answer.name + " added to playlist!");
            }

            // перерисовка плейлиста визуально
            await reload_playlist(playList);
            await draw_playlist(playList);
            setHeight();

            await save_user_info();

            // если установлена галочка 'Сохранять локально при добавлении в плейлист',
            //   то скачиваем файл в indexeddb
            const usr = await db.user.where('username').equals(user.username).first();
            if (usr) {
                if (usr.savelocal) {
                    await save_music_file(this.id.slice(8));
                }
            }
        } else {
            let answer = await resp.json()
            console.log(answer);
        }
    } catch (err) {
        alert("Сервер недоступен");
    }
}

async function search() {
    // Очищаем результаты предыдущего поиска
    result_table.innerHTML = "";

    // Изменяем текст на кнопке
    search_button.textContent = "Загрузка...";
    result_table.style.cursor = "wait";
    search_input.style.cursor = "wait";
    search_button.style.cursor = "wait";

    // Если в базе в истории запросов нет такого запроса, добавляем
    let req = await db.requests.where('request').equals(search_input.value).first();
    if (!req) {
        await db.requests.add({request: search_input.value});
    }

    try {
        let response = await fetch(
            GENERAL_ENDPOINT + "/search/?q=" + search_input.value
        );

        if (response.status === 200) {
            let json_data = await response.json();

            search_results = json_data;
            for (let item in json_data) {
                let new_tr = document.createElement("tr");
                result_table.appendChild(new_tr);

                let new_song_title = document.createElement("td");
                new_tr.appendChild(new_song_title);

                new_song_title.id = `rs_song_${json_data[item].url}`;
                new_song_title.className = "pl-song-title srch text-break";
                new_song_title.textContent = json_data[item].name;
                new_song_title.addEventListener("click", play_song);

                let new_td_2 = document.createElement("td");
                new_tr.appendChild(new_td_2);
                new_td_2.className = "rs-song-artist text-center";
                new_td_2.textContent = json_data[item].author ?? "";

                let new_td_3 = document.createElement("td");
                new_tr.appendChild(new_td_3);
                new_td_3.className = "pl-song-duration_text text-center";
                new_td_3.textContent = json_data[item].duration_text;

                let new_td_4 = document.createElement("td");
                new_tr.appendChild(new_td_4);

                let new_add_button = document.createElement("input");
                // new_td_4.appendChild(new_add_button);
                new_tr.appendChild(new_add_button)

                new_td_4.className = "text-center";
                new_add_button.type = "button";
                new_add_button.id = `add_btn_${json_data[item].url}`;
                new_add_button.className = "btn btn-dark btn-sm rm-btn";
                new_add_button.value = "+";
                new_add_button.addEventListener("click", add_song_to_playlist);

                search_input.value = "";
            }
        }
        if (response.status === 408) {
            alert("Сервера с музыкой отвечают слишком долго. Попробуйте ещё раз.");
            console.log("Request timeout");
        }
    } catch (error) {
        alert("Сервер недоступен");
        console.error("Error fetching data:", error);
    } finally {
        // Возвращаем исходный текст на кнопке
        search_button.textContent = "Найти";
        result_table.style.cursor = "default";
        search_input.style.cursor = "text";
        search_button.style.cursor = "default";
    }
}

search_button.addEventListener("click", search);

const choose_playlist_button = document.getElementById("ch-pl-btn");
const create_playlist_button = document.getElementById("cr-pl-btn");
const delete_playlist_button = document.getElementById("del-pl-btn");

const exampleModal = document.getElementById("exampleModal");
const modal_body = document.getElementById("cr-pl_body");

choose_playlist_button.addEventListener("click", choose_playlist);
create_playlist_button.addEventListener("click", create_playlist);
delete_playlist_button.addEventListener("click", delete_playlist);

async function choose_playlist() {
    const choosePlaylistModal = new bootstrap.Modal("#exampleModal");
    modal_body.innerHTML = "";
    choosePlaylistModal.show();

    for (item of allPlaylists) {
        let new_div = document.createElement("div");
        modal_body.appendChild(new_div);

        new_div.className = "";
        new_div.id = item.id;
        new_div.textContent = item.name + "(композиций: " + item.songs.length + ")";
        new_div.style.cursor = "default";
        new_div.addEventListener("click", async () => {
            for (let i of allPlaylists) {
                if (new_div.id == i.id) {
                    playList = i;
                    await draw_playlist(playList);
                    // закрываем окно
                    await choosePlaylistModal.hide();
                    break;
                }
            }
        });
    }
}

async function create_playlist() {
    const createPlaylistModal = new bootstrap.Modal("#cr-pl-modal");
    createPlaylistModal.show();

    const cr_input = document.getElementById("cr-pl-name");
    const cr_pl_button = document.getElementById("cr-pl-button");

    cr_input.value = "";

    async function handlePlaylistCreation() {
        cr_pl_button.removeEventListener("click", handlePlaylistCreation);
        try {
            let resp = await fetch(GENERAL_ENDPOINT + `/playlist/`, {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json;charset=utf-8",
                    Authorization: "Token " + getCookie("auth_token"),
                },
                body: JSON.stringify({name: cr_input.value}),
            });
            if (resp.ok) {
                let answer = await resp.json();      // Получить JSON ответ от сервера
                console.log("Playlist created " + answer.name);
                createPlaylistModal.hide();
                await load_playlists();
                for (i of allPlaylists) {
                    if (answer.name == i.name) {
                        playList = i;
                        await draw_playlist(playList);
                        break;
                    }
                }
            }
        } catch (err) {
            alert("Сервер недоступен");
            console.log(err);
        }
    }

    cr_pl_button.addEventListener("click", handlePlaylistCreation);
}

async function delete_playlist() {
    if (confirm("Внимание! Вы удаляете плейлист " + playList.name)) {
        try {
            let resp = await fetch(
                GENERAL_ENDPOINT + "/playlist/" + playList.id + "/",
                {
                    method: "DELETE",
                    headers: {
                        Accept: "application/json",
                        Authorization: "Token " + getCookie("auth_token"),
                    },
                }
            );
            if (resp.ok) {
                console.log("Playlist deleted!");
                await load_playlists();
                if (allPlaylists.length > 0) {
                    playList = allPlaylists[0];
                    await draw_playlist(playList);
                } else {
                    playList = {
                        name: "-//-",
                        songs: []
                    };
                    await draw_playlist(playList);
                }
                ;
            }
            ;
        } catch (error) {
            alert("Сервер недоступен");
            console.error("Error deleting playlist: ", error);
        }
    } else {
        console.log("Удаление плейлиста отменено пользователем.");
    }
}
