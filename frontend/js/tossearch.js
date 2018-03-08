/*jshint esversion: 6 */

/* --------------
  ReadyHelper
----------------*/
class ReadyHelper {
  constructor(callback) {
    this.readys = {
      typeahead: false,
      dictionary: false,
      dictionary_en: false,
      document: false
    };
    this.callback = callback;
  }
  setReady(id) {
    this.readys[id] = true;
    this.checkReady();
  }
  checkReady() {
    let allready = true;
    $.each(this.readys, function (index, value) {
      allready &= value;
    }); 
    if (allready) this.callback();
  }
}


/* --------------
  TypeaheadHelper
----------------*/
var TypeaheadHelper = function() {
  let engine = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace(['en', 'tw']),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    identify: function (obj) { return obj.ClassID; },
    prefetch: 'data/result_list.json',
    initialize: false
  });
  this.items_en = engine;
  var promise = engine.initialize();
  promise.done(function() {
    readyHelper.setReady('typeahead');
    console.log("typeahead ready");
  }).fail(function() {
    console.log("typeahead error");
  });
};

TypeaheadHelper.prototype.action = function () {
  $('.typeahead').typeahead(null, {
    name: 'items-en',
    source: this.items_en,
    display: function(obj) {
      return obj.en;
    },
    limit: 100,
    templates: {
      suggestion: this.suggestion
    }
  });
};

TypeaheadHelper.prototype.suggestion = function(data) {
  input_val = $('#search-content').val();
  let hasChinese = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]/.test(input_val);
  let imgstr = '<img src="https://tos.neet.tv' + data.img + '" width="18" height="18"> ';
  let lang1 = hasChinese ? data.tw: data.en;
  let lang2 = hasChinese ? data.en : data.tw;
  lang1 = '<strong>' + lang1 + '</strong>';
  lang2 = '(' + lang2 + ')';
  return '<div>' + imgstr + lang1 + lang2 + '</div>';
};


/* --------------
  SearchMod
----------------*/
var TosSearchMod = function () {
  this.dictionary = {};
  this.dictionary_tw = {};
  this.readData(this);
};

TosSearchMod.prototype.readData = function(self) {
  $.getJSON("data/tables_en.json", function (data) {
    console.log("Dictionary loaded");
    readyHelper.setReady('dictionary');
    // Cannot use this here due to jQuery
    self.dictionary = data;
  });
  $.getJSON("data/tables_tw.json", function (data) {
    console.log("Dictionary-tw loaded");
    readyHelper.setReady('dictionary_en');
    self.dictionary_tw = data;
  });
};

TosSearchMod.prototype.search = function(val, cb_success, cb_fail) {
  console.log("Searching: " + val);
  let entry = this.dictionary[val];
  if (!entry) entry = this.dictionary_tw[val];
  if (entry) {
    let classID = entry.ClassID;
    let category = entry.category;
    this.openpage(category, classID);
    if (cb_success) cb_success();
  } else {
    console.log("ClassID Not Found.");
    if (cb_fail) cb_fail();
  }
};

TosSearchMod.prototype.openpage = function (category, classID) {
  let url = 'https://tos.neet.tv/' + category + '/' + classID;
  window.open(url);
};


/* --------------
  main
----------------*/

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("tosquery").style.display = "block";
}

var readyHelper = new ReadyHelper(function () {
  console.log("ALL READY");
  showPage();
});
var typeaheadHelper = new TypeaheadHelper();
var searchmod = new TosSearchMod();

$(document).ready(function () {
  console.log("DOM ready!");
  readyHelper.setReady('document');

  typeaheadHelper.action();
  $('.typeahead').bind('typeahead:select', function (ev, suggestion) {
    searchmod.search(suggestion.en);
  });
  $('#search').click(function () {
    let val = $('#search-content').val();
    val = val.replace(/\b\w/g, l => l.toUpperCase());
    searchmod.search(val, function cb_success() {
      $('#notfound-indicator').html('');
    }, function cb_fail() {
      if ($(".tt-suggestion").length) {
        $(".tt-suggestion").first().trigger('click');
        $('#notfound-indicator').html('');
      } else {
        $('#notfound-indicator').html('Not Found');
      }
    });
  });
  // Listen to Enter Key
  // Use 'keypress' instead of 'keyup' to avoid Chinese input issue (wbkuo.pixnet.net/blog/post/191525544-[javascript]-解決使用新注音輸入時選字按-enter-)
  $('.typeahead').on('keypress', function (e) {
    if (e.which == 13) $('#search').trigger('click');
  });
  
  tippy('.tippy');
});
