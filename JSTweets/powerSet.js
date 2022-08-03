function powerSet2(set) {
    let powSetSize = Math.pow(2, set.length);
    let str = ""
    for (let counter = 0; counter < powSetSize; counter++) {
        for (let j = 0; j < set.length; j++)
            if ((counter & (1 << j)) > 0) str += set[j];
        console.log(str); str = "";
    }
}





function powerSet(set, i, subset) {
    if (i === set.length) {
        console.log(subset);
        return;
    }
    powerSet(set, i + 1, [...subset, set[i]])
    powerSet(set, i + 1, subset)
}

powerSet(['a','b','c'], 0, [])



