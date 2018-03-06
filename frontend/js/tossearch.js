var items_en = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  // url points to a json file that contains an array of country names, see
  // https://github.com/twitter/typeahead.js/blob/gh-pages/data/countries.json
  prefetch: 'data/names_en.json'
});

var items_tw = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: 'data/names_tw.json'
});

$(document).ready(function () {
  console.log("ready!");
  // passing in `null` for the `options` arguments will result in the default
  // options being used
  $('#prefetch .typeahead').typeahead(null, {
    name: 'items-en',
    source: items_en
  }, {
    name: 'items-tw',
    source: items_tw
  });

  $('.typeahead').bind('typeahead:select', function (ev, suggestion) {
    console.log('Selection: ' + suggestion);
  });
});