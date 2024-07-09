const APP_ID = '0eb423f7127d4e1bbdaa5b4bbb5994b9';
const TOKEN = sessionStorage.getItem('token');
const USER_ID = sessionStorage.getItem('user_id');
const RECEIVER = sessionStorage.getItem('fullname');
let UID = sessionStorage.getItem('UID');

let NAME = sessionStorage.getItem('fullname');

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

console.log(client);

let localTracks = [];
let remoteUsers = {};

let joinAndDisplayLocalStream = async () => {
    // document.getElementById('room-name').innerText = USER_ID;

    client.on('user-published', handleUserJoined);
    client.on('user-left', handleUserLeft);

    try {
        UID = await client.join(APP_ID, USER_ID, TOKEN, UID);
    } catch (error) {
        console.error(error);
        window.open('/', '_self');
    }

    try {
        localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();

        let member = await createMember();

        let player = `<div class="video-container" id="user-container-${UID}">
                        <div class="video-player" id="user-${UID}"></div>
                        <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                    </div>`;

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);
        localTracks[1].play(`user-${UID}`);
        await client.publish([localTracks[0], localTracks[1]]);
    } catch (error) {
        console.error('Failed to create and display local tracks:', error);
    }
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user;
    await client.subscribe(user, mediaType);

    if (mediaType === 'video') {
        let player = document.getElementById(`user-container-${user.uid}`);
        if (player != null) {
            player.remove();
        }

        let member = await getMember(user);

        player = `<div class="video-container" id="user-container-${user.uid}">
                    <div class="video-player" id="user-${user.uid}"></div>
                    <div class="username-wrapper"><span class="user-name">${RECEIVER}</span></div>
                  </div>`;

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player);
        user.videoTrack.play(`user-${user.uid}`);
    }

    if (mediaType === 'audio') {
        user.audioTrack.play();
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid];
    let player = document.getElementById(`user-container-${user.uid}`);
    if (player) {
        player.remove();
    }
}

let leaveAndRemoveLocalStream = async () => {
    for (let i = 0; i < localTracks.length; i++) {
        localTracks[i].stop();
        localTracks[i].close();
    }

    await client.leave();
    deleteMember();
    window.close();
}

let toggleCamera = async (e) => {
    console.log('TOGGLE CAMERA TRIGGERED');
    if (localTracks[1].muted) {
        await localTracks[1].setMuted(false);
        e.target.style.backgroundColor = '#fff';
    } else {
        await localTracks[1].setMuted(true);
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)';
    }
}

let toggleMic = async (e) => {
    console.log('TOGGLE MIC TRIGGERED');
    if (localTracks[0].muted) {
        await localTracks[0].setMuted(false);
        e.target.style.backgroundColor = '#fff';
    } else {
        await localTracks[0].setMuted(true);
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)';
    }
}

let createMember = async () => {
    try {
        let response = await fetch(`create_member/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'name': NAME, 'room_name': USER_ID, 'UID': UID })
        });

        if (!response.ok) {
            throw new Error('Failed to create member');
        }

        let member = await response.json();
        console.log(member);
        return member;
    } catch (error) {
        console.error('Error creating member:', error);
        return null;
    }
}

let getMember = async (user) => {
    try {
        let response = await fetch(`http://127.0.0.1:8000/call/video/get_member/?UID=${user.uid}&room_name=${USER_ID}`);

        if (!response.ok) {
            throw new Error('Failed to get member');
        }

        let member = await response.json();
        return member;
    } catch (error) {
        console.error('Error getting member:', error);
        return null;
    }
}

let deleteMember = async () => {
    try {
        let response = await fetch('http://127.0.0.1:8000/call/video/delete_member/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'name': NAME, 'room_name': USER_ID, 'UID': UID })
        });

        if (!response.ok) {
            throw new Error('Failed to delete member');
        }

        let member = await response.json();
    } catch (error) {
        console.error('Error deleting member:', error);
    }
}

window.addEventListener("beforeunload", deleteMember);

joinAndDisplayLocalStream();

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream);
document.getElementById('camera-btn').addEventListener('click', toggleCamera);
document.getElementById('mic-btn').addEventListener('click', toggleMic);
