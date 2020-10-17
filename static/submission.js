//Counts for number of each next section that's going to be added
let categoryCount = 2;
let subcategoryCount = 2;
let tradeCount = 2;
let issueCount = 2;
let partCount = 2;
let issuePartCount = 2;
let clickCount = 0;

//Event handlers for button clicks
//Event handler for adding additional sections for submission
$('body').on('click', async function(e) {
	if (e.target.localName == 'button' && e.target.innerText != 'Submit' && e.target.id != 'fix') {
		e.preventDefault();
		if (e.target.id == 'add-category') {
			e.target.remove();
			$('#AddCategory #container').append(`
                        <div>
                        <label for="name${categoryCount}">Category ${categoryCount}:</label>
                        <input type="text" name="name${categoryCount}">    
                        <button id="add-category">Add Additional category</button> 
                        </div>
                        `);
			categoryCount++;
		}

		if (e.target.id == 'add-subcategory') {
			e.target.remove();
			$('#AddSubcategory #container').append(`
		                <div>
		                <label for="subcategory${subcategoryCount}">Subcategory ${subcategoryCount}:</label>
		                <input type="text" name="subcategory${subcategoryCount}">
		                <button id="add-subcategory">Add</button>
		                </div>
		        `);
			subcategoryCount++;
		}

		if (e.target.id == 'add-trade') {
			console.log(e.target);
			e.target.remove();
			$('#AddTrade #container').append(`
						<div id="tradeHolder${tradeCount}>
                        <h3>Trade ${tradeCount}</h3>    
                        <div>
                        <label for="name${tradeCount}">Name:</label>
                        <input type="text" name="name${tradeCount}" id="trade-name${tradeCount}">
                        </div>
                        <div>
                        <label for="cost${tradeCount}">Cost per hour:</label>
                        <input type="text" name="cost${tradeCount}" id="trade-cost${tradeCount}">    
                        </div>
                        <button id="add-trade">Add Additional Trade</button>
						</div>
						`);
			tradeCount++;
		}

		if (e.target.id == 'add-issue') {
			console.log(e.target);
			e.target.remove();
			$('#AddIssue #container').append(`
						<div id=issueHolder${issueCount}>
                        <h3>Issue ${issueCount}</h3>    
                        <div>
                        <label for="name${issueCount}">Name:</label>
                        <input type="text" name="issue-name${issueCount}" id="issue-name${issueCount}">
                        </div>
                        <div>
                        <label for="video${issueCount}">Video URL:</label>
                        <input type="text" name="video${issueCount}" id="video${issueCount}">    
                        </div>
                        <div>
                        <label for="hours${issueCount}">Number of Hours To Complete:</label>
                        <input type="text" name="hours${issueCount}" id="hours${issueCount}">    
                        </div>
                        <div>
                        <label for="difficulty${issueCount}">Difficulty:</label>
                        <select name="difficulty${issueCount}" id="difficulty${issueCount}">
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option> 
                        </select>  
                        </div>
                        <button id="add-issue">Add Additional Issue</button> 
						</div>
						</div>
                        `);
			issueCount++;
		}

		if (e.target.id == 'add-part') {
			e.target.remove();
			$('#AddPart #container').append(`
                        <div>
                        <label for="part${partCount}">Part ${partCount}:</label>
                        <input type="text" name="part${partCount}" id="part${partCount}">    
                        <button id="add-part">Add Additional part</button> 
                        </div>
                        `);
			partCount++;
		}

		//Feature coming: Allow multiple issuepart submissions at once, need to update current route to accept json
		// if (e.target.id == 'add-issuepart') {
		// 	e.target.remove();
		// 	$('#AddIssuePart #container').append(`
		//         <div id=${issuePartCount}>
		//         <label for="part">Part ${issuePartCount}:</label>
		//         <select name="part" id="issue-part-part${issuePartCount}">
		// 		</select>
		// 		<label for="issue">Issue ${issuePartCount}:</label>
		//         <select name="issue" id="issue-part-issue${issuePartCount}">
		//         </select>
		//         </div>
		//         <button id="add-issuepart">Add Additional part</button>
		// 		`);
		// 	let issue_parts = await axios.get('/api/issue-parts');
		// 	for (part of issue_parts.data.response.parts) {
		// 		$(`#issue-part-part${issuePartCount}`).append(`<option value=${part}>${part}`);
		// 	}
		// 	for (issue of issue_parts.data.response.issues) {
		// 		$(`#issue-part-issue${issuePartCount}`).append(`<option value=${issue}>${issue}`);
		// 	}
		// 	issuePartCount++;
		// }
	}
});

//When section for adding new instance is selected
$('#creation-selector > button').on('click', function(e) {
	$('#creation-selector').toggle('hidden');
	$(`#${e.target.innerText.replaceAll(' ', '')}`).show();
	$('#back').toggle('hidden');
	selectedSection = e.target.innerText.replaceAll(' ', '');
});

//When back button is clicked
$('#back').on('click', function(e) {
	e.preventDefault();
	$('#creation-selector').toggle('hidden');
	$(`#${selectedSection}`).hide();
	$('#back').toggle('hidden');
});

//When submit button is clicked for Issue section
$('#submit-issue').on('click', function(e) {
	e.preventDefault();
	submitIssue();
	location.reload();
});

//When submit button is clicked for Trade section
$('#submit-trade').on('click', function(e) {
	e.preventDefault();
	submitTrade();
});

//When submit button is clicked for Part section
$('#submit-part').on('click', function(e) {
	e.preventDefault();
	submitPart();
});

//Functions for handling submissions
//Function for submitting issues
async function submitIssue() {
	issueCount--;
	for (i = 1; i <= issueCount; i++) {
		if (i == 1) {
			await axios.post('/add-issue', {
				name: $('#issue-name').val(),
				subcategory: $('#issue-subcategory').val(),
				video_url: $(`#video`).val(),
				num_hours: $(`#hours`).val(),
				difficulty: $(`#difficulty`).val()
			});
			$('#issue-name').val('');
			$(`#video`).val('');
			$(`#hours`).val('');
			$(`#difficulty`).val('');
		} else {
			await axios.post('/add-issue', {
				name: $(`#issue-name${i}`).val(),
				subcategory: $('#issue-subcategory').val(),
				video_url: $(`#video${i}`).val(),
				num_hours: $(`#hours${i}`).val(),
				difficulty: $(`#difficulty${i}`).val()
			});
			$(`#issueHolder${i}`).remove();
		}
	}
	issueCount++;
	$('#creation-selector').toggle('hidden');
	$(`#${selectedSection}`).hide();
	if ($(`#flash-messages`).text() == '') {
		$('body').prepend('<div id=flash-messages>');
		if (issueCount <= 2) {
			$('#flash-messages').text('Issue sent to database');
		} else {
			$('#flash-messages').text('Multiple Issues sent to database');
		}
	} else {
		if (issueCount <= 2) {
			$('#flash-messages').text('Issue sent to database');
		} else {
			$('#flash-messages').text('Multiple Issues sent to database');
		}
	}
	issueCount = 2;
	$('#back').toggle('hidden');
}

//Function for submitting trades
async function submitTrade() {
	tradeCount--;
	for (i = 1; i <= tradeCount; i++) {
		if (i == 1) {
			await axios.post('/add-trade', {
				category: $('#trade-category').val(),
				name: $(`#trade-name`).val(),
				cost: $(`#trade-cost`).val()
			});
			$(`#trade-name`).val('');
			$(`#trade-cost`).val('');
		} else {
			await axios.post('/add-trade', {
				category: $('#trade-category').val(),
				name: $(`#trade-name${i}`).val(),
				cost: $(`#trade-cost${i}`).val()
			});
			$(`#tradeHolder${i}`).remove();
		}
	}
	tradeCount++;
	$('#creation-selector').toggle('hidden');
	$(`#${selectedSection}`).hide();
	if ($(`#flash-messages`).text() == '') {
		$('body').prepend('<div id=flash-messages>');
		if (tradeCount <= 2) {
			$('#flash-messages').text('Trade sent to database');
		} else {
			$('#flash-messages').text('Multiple Trades sent to database');
		}
	} else {
		if (tradeCount <= 2) {
			$('#flash-messages').text('Trade sent to database');
		} else {
			$('#flash-messages').text('Multiple Trades sent to database');
		}
	}
	tradeCount = 2;
	$('#back').toggle('hidden');
}

//Function for submitting parts
async function submitPart() {
	partCount--;
	for (i = 1; i <= partCount; i++) {
		if (i == 1) {
			await productSearch($('#part').val());
			if (searchResults.responseMessage == 'Product successfully found!') {
				let j = 0;
				let productLinksArray = searchResults.foundProducts;
				productLinksArray = productLinksArray.slice(0, 5);
				$('#link-holder').append('<div id=links>');
				for (product of productLinksArray) {
					product = product.replaceAll('"', '');
					link = `<li><a href="https://walmart.com${product}" target="_blank">${j}</a><button id=links-button-${j}>Select</button><button id=submit-links-button${j} style="display: none">Confirm</button></li>`;
					$('#links').append(link);
					$(`#links-button-${j}`).on('click', function(e) {
						e.preventDefault();
						confirmId = e.target.nextSibling.id;
						$(`#${confirmId}`).toggle('hidden');
						$(`#${confirmId}`).on('click', async function(e) {
							e.preventDefault();
							let productData = await getProductData(
								searchResults.foundProducts[e.target.parentNode.children[0].text]
							);
							let name = product;
							e.target.parentNode.parentNode.remove();
							chicken = axios.post('/add-part', {
								name: $('#part').val(),
								price: productData.price,
								link: `https://walmart.com${searchResults.foundProducts[
									e.target.parentNode.children[0].text
								]}`,
								image_url: productData.imageUrlList[0]
							});
							$('#part').val('');
							partCount--;
							clickCount++;
							if (partCount == 0) {
								$('#back').trigger('click');
								if (clickCount > 1) {
									if ($(`#flash-messages`).text() == '') {
										$('body').prepend('<div id=flash-messages>');
										$('#flash-messages').text('Multiple parts sent to database');
									} else {
										$('#flash-messages').text('Multiple parts sent to database');
									}
								} else {
									if ($(`#flash-messages`).text() == '') {
										$('body').prepend('<div id=flash-messages>');
										$('#flash-messages').text('Part sent to database');
									} else {
										$('#flash-messages').text('Part sent to database');
									}
								}
								clickCount = 0;
								partCount = 2;
							} else {
								// console.log(clickCount);
								// clickCount++;
							}
						});
					});
					j++;
				}
			} else {
				$(`#links`).append('<h1>Product Not Found!</h1>');
			}
		} else {
			await productSearch($(`#part${i}`).val());
			if (searchResults.responseMessage == 'Product successfully found!') {
				let j = 0;
				let productLinksArray = searchResults.foundProducts;
				productLinksArray = productLinksArray.slice(0, 5);
				$('#link-holder').append(`<div id=links${i}>`);
				for (product of productLinksArray) {
					productQuery = product.replaceAll('"', '');
					link = `<li><a href="https://walmart.com${productQuery}" target="_blank">${j}</a><button id=links${i}-button-${j}>Select</button><button id=submit-links${i}-button-${j} style="display: none">Confirm</button></li>`;
					console.log(i);
					$(`#links${i}`).append(link);
					$(`#links${i}-button-${j}`).on('click', function(e) {
						e.preventDefault();
						confirmId = e.target.nextSibling.id;
						$(`#${confirmId}`).toggle('hidden');
						$(`#${confirmId}`).on('click', async function(e) {
							e.preventDefault();
							console.log(i);
							let productData = await getProductData(
								searchResults.foundProducts[e.target.parentNode.children[0].text]
							);
							let name = product;
							e.target.parentNode.parentNode.remove();
							axios.post('/add-part', {
								name: $(`#part${i - 1}`).val(),
								price: productData.price,
								link: `https://walmart.com${searchResults.foundProducts[
									e.target.parentNode.children[0].text
								]}`,
								image_url: productData.imageUrlList[0]
							});
							console.log(partCount);
							partCount--;
							console.log(partCount);
							$(`#part${i - 1}`).parent().remove();
							clickCount++;
							if (partCount == 0) {
								$('#back').trigger('click');
								if (clickCount > 1) {
									if ($(`#flash-messages`).text() == '') {
										$('body').prepend('<div id=flash-messages>');
										$('#flash-messages').text('Multiple parts sent to database');
									} else {
										$('#flash-messages').text('Multiple parts sent to database');
									}
								} else {
									if ($(`#flash-messages`).text() == '') {
										$('body').prepend('<div id=flash-messages>');
										$('#flash-messages').text('Part sent to database');
									} else {
										$('#flash-messages').text('Part sent to database');
									}
								}
								clickCount = 0;
								partCount = 2;
							} else {
								// console.log(clickCount);
								// clickCount++;
							}
						});
					});

					j++;
				}
			} else {
				$(`#links${i}`).append('<h1>Product Not Found!</h1>');
			}
		}
	}
}

//Handle product search and walmart API requests
async function productSearch(product) {
	/* 
	 Successful query response data:
	 foundProducts: (20) ["/ip/NBA-2K21-Mamba-Forever-Edition-2K-PlayStation-…4&wpa_tax=2636_1102672_1106096&wpa_bucket=__bkt__", "/ip/Sony-PlayStation-4-1TB-Slim-Gaming-Console/101507200", "/ip/Sony-PlayStation-4-Pro-1TB-Gaming-Console-Wireless-Game-Pad-Black/741505081", "/ip/Sony-PlayStation-4-500GB-Slim-System-Black/406966077", "/ip/Sony-PlayStation-Slim-4-1TB-Only-on-PlayStation-PS4-Console-Bundle-Black/431121707", "/ip/Sony-PlayStation-Slim-1TB-Fortnite-Neo-Versa-PS4-Bundle/262620661", "/ip/Sony-PlayStation-4-Slim-1TB-Gaming-Console-Black-CUH-2115B/782841840", "/ip/Refurbished-Sony-PlayStation-4-1TB-Slim-Gaming-Console-CUH-2215BB01/281166119", "/ip/Grand-Theft-Auto-V-Premium-Edition-Rockstar-Games-PlayStation-4-710425570322/280167762", "/ip/Sony-PlayStation-4-Slim-500GB-Gaming-Console-Black-CUH-2115A/536117094", "/ip/Sony-PlayStation-4-Slim-1TB-Spiderman-Bundle-Black-CUH-2215B/579371947", "/ip/NBA-2K20-2K-PlayStation-4-710425575259/800844155", "/ip/Sony-PlayStation-4-DualShock-4-Controller-Gold/456975565", "/ip/Call-of-Duty-Modern-Warfare-Activision-PlayStation-4-0047875884359/615027923", "/ip/Sony-Playstation-4-DualShock-4-Controller-Midnight-Blue/268238851", "/ip/Sony-PlayStation-4-1TB-Slim-Days-of-Play-Limited-Edition-Blue-3003131/829692281", "/ip/Sony-PlayStation-4-1TB-Slim-System-w-Call-of-Duty-Black-Ops-4-3003223/838048611", "/ip/Mortal-Kombat-XL-Warner-Bros-PlayStation-4-883929527458/49593184", "/ip/Marvel-s-Spider-Man-Game-of-the-Year-Edition-Sony-PlayStation-4-711719529958/563250456", "/ip/Plants-vs-Zombies-Battle-for-Neighborville-Electronic-Arts-PlayStation-4-014633370768/978268406"]
	 keyword: "Playstation 4"
	 numberOfProducts: 20
	 responseMessage: "Product successfully found!"
	 responseStatus: "PRODUCT_FOUND_RESPONSE" */

	product = product.replaceAll(' ', '%20');

	settings = {
		async: true,
		crossDomain: true,
		url: `https://axesso-walmart-data-service.p.rapidapi.com/wlm/walmart-search-by-keyword?sortBy=best_match&page=1&keyword=${product}&type=text`,
		method: 'GET',
		headers: {
			'x-rapidapi-host': 'axesso-walmart-data-service.p.rapidapi.com',
			'x-rapidapi-key': '35e13ce044msh7591bf9e2e4a549p157b1djsn1a838914571a'
		}
	};

	searchResults = await $.ajax(settings).done(function(response) {
		return response;
	});

	// Shows first five links from product search for determining product to use
	return searchResults;
}

async function getProductData(productLink) {
	/*
Successful request will return:

"responseMessage":"Product successfully found!"
"productTitle":"X Rocker X-Pro 300 Black Pedestal Gaming Chair Rocker with Built-in Speakers"
"manufacturer":"X Rocker"
"walmartItemId":554348865
"price":108

*/

	settings = {
		async: true,
		crossDomain: true,
		url: `https://axesso-walmart-data-service.p.rapidapi.com/wlm/walmart-lookup-product?url=https://walmart.com${productLink}`,
		method: 'GET',
		headers: {
			'x-rapidapi-host': 'axesso-walmart-data-service.p.rapidapi.com',
			'x-rapidapi-key': '35e13ce044msh7591bf9e2e4a549p157b1djsn1a838914571a'
		}
	};

	productData = await $.ajax(settings).done(function(response) {
		return response;
	});

	return productData;
}
