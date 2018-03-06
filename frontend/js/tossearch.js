/*jshint esversion: 6 */

/* --------------
  TypeaheadHelper
----------------*/
var TypeaheadHelper = function() {
  this.items_en = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    // url points to a json file that contains an array of country names, see
    // https://github.com/twitter/typeahead.js/blob/gh-pages/data/countries.json
    prefetch: 'data/names_en.json'
  });
  this.items_tw = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: 'data/names_tw.json'
  });
};

TypeaheadHelper.prototype.action = function () {
  // passing in `null` for the `options` arguments will result in the default
  // options being used
  $('#prefetch .typeahead').typeahead(null, {
    name: 'items-en',
    source: this.items_en
  }, {
    name: 'items-tw',
    source: this.items_tw
  });
};


/* --------------
  SearchMod
----------------*/
var TosSearchMod = function () {
  this.dictionary = {};
  this.readData(this);
};

TosSearchMod.prototype.readData = function(self) {
  $.getJSON("data/tables_en.json", function (data) {
    console.log("Dictionary loaded");
    // Cannot use this here due to jQuery
    self.dictionary = data;
  });
};

TosSearchMod.prototype.search = function(val) {
  console.log("Searching: " + val);
  let classID = this.dictionary[val]['ClassID'];
  if (classID) {
    console.log("ClassID:" + classID);
  } else {
    console.log("ClassID Not Found.");
  }
};


/* --------------
  main
----------------*/

var typeaheadHelper = new TypeaheadHelper();
var searchmod = new TosSearchMod();

$(document).ready(function () {
  console.log("ready!");
  typeaheadHelper.action();

  $('.typeahead').bind('typeahead:select', function (ev, suggestion) {
    console.log('Selection: ' + suggestion);
  });

  $('#search').click(function () {
    searchmod.search($('#search-content').val())
  });
});
