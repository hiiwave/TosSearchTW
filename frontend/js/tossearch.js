/*jshint esversion: 6 */

/* --------------
  TypeaheadHelper
----------------*/
var TypeaheadHelper = function() {
  this.items_en = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace(['en', 'tw']),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    identify: function (obj) { return obj.ClassID; },
    prefetch: 'data/result_list.json'
  });
  this.firstSuggestion = {};
};

TypeaheadHelper.prototype.action = function () {
  $('.typeahead').typeahead(null, {
    name: 'items-en',
    source: this.items_en,
    display: function(obj) {
      return obj.en;
    },
    templates: {
      suggestion: this.suggestion
    }
  });
};

TypeaheadHelper.prototype.suggestion = function(data) {
  input_val = $('#search-content').val();
  let hasChinese = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]/.test(input_val);
  if (hasChinese) {
    return '<div><strong>' + data.tw + '</strong> (' + data.en + ')</div>';
  } else {
    return '<div><strong>' + data.en + '</strong> (' + data.tw + ')</div>';
  }  
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

TosSearchMod.prototype.search = function(val, cb_fail) {
  console.log("Searching: " + val);
  let entry = this.dictionary[val];
  if (entry) {
    let classID = entry.ClassID;
    console.log("ClassID:" + classID);
    this.openpage(classID);
  } else {
    console.log("ClassID Not Found.");
    cb_fail();
  }
};

TosSearchMod.prototype.openpage = function(classID) {
  let url = 'https://tos.neet.tv/items/' + classID;
  window.open(url);
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
    searchmod.search(suggestion.en);
  });

  $('#search').click(function () {
    $(".tt-suggestion").first().trigger('click')
    // let val = $('#search-content').val();
    // searchmod.search(val, function() {
    //   $('#notfound-indicator').html('Not Found');
    // });
  });

  tippy('.tippy');

  // $('.typeahead').on('keyup', function (e) {
  //   if (e.which == 13) {
  //     $(".tt-suggestion").first().trigger('click');
  //   }
  // });
});
