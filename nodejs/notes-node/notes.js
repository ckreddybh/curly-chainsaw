const fs = require('fs');

var fetchNotes = () => {
    try{
        return JSON.parse(fs.readFileSync('notes-data.json'));
    } catch(e){
        return [];
    }
};

var saveNotes = (notes) => {
    fs.writeFileSync('notes-data.json', JSON.stringify(notes));
};

var addNotes = (title, body) => {
    console.log("Adding notes: ", title, body);
    var notes = fetchNotes();

    var note = {
        title,
        body
    };

    var duplicateNotes = notes.filter((note) => note.title === title );

    if (duplicateNotes.length === 0){
        notes.push(note);
        saveNotes(notes);
        return note;
    }
};

var getAllNotes = () => {
    console.log("Getting all notes");
    var notes = fetchNotes();
    return notes;
};

var removeNotes = (title) => {
    var notes = fetchNotes();
    var filteredNotes = notes.filter((note) => note.title !== title );
    saveNotes(filteredNotes);
    return notes.length > 0 ? notes.length !== filteredNotes.length : false;
};

var readNotes = (title) => {
    console.log("reading note : ", title);
    var notes = fetchNotes();
    return notes.filter((note) => note.title === title)[0 ];
};

var logNote = (note) => {
    console.log('---');
    console.log('Title: '+note.title+'\nBody: '+note.body);
};

module.exports = {
    addNotes,
    getAllNotes,
    removeNotes: removeNotes,
    readNotes,
    logNote
};
