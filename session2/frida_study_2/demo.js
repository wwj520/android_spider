function hook() {
    console.log(11)

    Java.perform(function () {
        let MainActivity = Java.use("com.kanxue.ollvm_ndk.MainActivity");
        MainActivity.UUIDCheckSum.implementation = function (str) {
            let ret = this.UUIDCheckSum(str);
            console.log("input: " + str + " output: " + ret);
            return ret;
        };
    });
}

function call_check_sum() {
    Java.perform(function () {
        let MainActivity = Java.use("com.kanxue.ollvm_ndk.MainActivity");
        var str = "DidDUaE35dQw4h3iUbGwuYzGGOIyC5bg92CE";
        var ret = MainActivity.UUIDCheckSum(str);
        console.log("input: " + str + " output: " + ret);
    });
}

setImmediate(hook)