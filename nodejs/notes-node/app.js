const yargs = require('yargs');

const notes = require('./notes.js');

const titleOptions = {
   describe: "title of hte note",
   demand: true,
   alias: 't'
};

const bodyOptions = {
    describe: "Body of note",
    demand: true,
    alias: 'b'
};

var args = yargs
    .command('add', 'Add new note', {
        title: titleOptions,
        body: bodyOptions
    })
    .command('remove', 'Remove a note', {
        title: titleOptions
    })
    .command('list', "List all notes")
    .command('read', 'Read a note', {
        title: titleOptions
    })
    .help()
    .argv

var command = args._[0]

if( command == 'add'){
    var note = notes.addNotes(args.title, args.body);
    if(note !== undefined){
        notes.logNote(note);
    }else{
        console.log("note with the title::  "+args.title+" ::already exist");
    }
} else if ( command == 'remove' ){
    var removed = notes.removeNotes(args.title);
    var message = removed ? "Note Deleted" : "Note Not Found";
    console.log(message);
} else if ( command == 'list'){
    var allnotes = notes.getAllNotes();
    if(allnotes !== []){
        var noteNotes = allnotes.length>1 ? "notes" : "note";
        console.log(`printing ${allnotes.length} ${noteNotes}`);
        allnotes.forEach((note) => notes.logNote(note));
    }else{
        console.log("No notes to show");
    }

} else if ( command == 'read'){
    var note = notes.readNotes(args.title);
    if(note){
        notes.logNote(note);
    }
    else{
        console.log("Note not found");
    }
}else {
    console.log('command not recognized');
}
