// References:
// http://javascript.crockford.com/private.html
// http://javascript.crockford.com/prototypal.html
// http://javascript.crockford.com/inheritance.html
// http://stackoverflow.com/questions/907225/object-oriented-javascript-best-practices
// http://stackoverflow.com/questions/387707/whats-the-best-way-to-define-a-class-in-javascript
// http://mckoss.com/jscript/object.htm
// http://phrogz.net/js/classes/OOPinJS.html
// http://phrogz.net/js/classes/OOPinJS2.html
// http://stackoverflow.com/questions/1595611/how-to-properly-create-a-custom-object-in-javascript
// http://stackoverflow.com/questions/874559/javascript-classes-no-frameworks
//
// Notes:
// console.log does not work in IE.
//
(function(window) {
    //////////////////////////////////
    // Namespace definition
    //
    if(typeof window.FruitNamespace == 'undefined') {
        window.FruitNamespace = {};
    }
    // We use the full namespace throughout this example,
    // but you could alias things to shorter, closure scope variables.
    // e.g. var Apple = FruitNamespace.Apple;
    var FruitNamespace = window.FruitNamespace;



    //////////////////////////////////
    // Class definition using prototype.
    //
    // Note: "this" references will be broken when methods are invoked via aliases.
    //
    (function() { // Closure for Orange.

        // The ctor initializes the object and is called every time for: "new Orange()"
        // this refers to the new object.
        // (Orange is just a property on the FruitNamespace object,
        // its value the function that acts as the constructor.)
        FruitNamespace.Orange = function(ctorArg1) {
            // This property (member) is "public". Each instance of Orange has its own copy.
            this.ctorArg1 = ctorArg1;
            console.log('Orange ctor() called.');
        };

        // We can declare the equivalent of static variables here (in closure scope),
        // but there's no way to create instance variables.
        var _orangeStaticVar = 'A private static variable for Oranges.';

        // Private static method, but "this" will be wrong unless we use call()/apply() as shown below.
        var _orangeClosureMethod = function(message) {
            var logMessage = '_orangeClosureMethod() called with arg: ' + message + '  this: ' + this + '   ';
            if(typeof this.getName != typeof Function) {
                logMessage += 'missing getName()';
            }
            else {
                logMessage += 'this.getName(): ' + this.getName();
            }
            logMessage += '  _orangeStaticVar: ' + _orangeStaticVar;
            console.log(logMessage);
        };

        // Public methods/members are declared on the prototype.
        //
        // The prototype definition is only executed once,
        // i.e. there is only one copy of these functions for all Oranges.
        FruitNamespace.Orange.prototype = {
            removePeel: function() {
                // this is the Orange normally, so we can call this.getName().
                // However, this won't work if the function is aliased! e.g. "var f = orangeInstance.removePeel; f();"
                console.log('removePeel() Removing Orange peel: ' + this.getName());
                // We must remember to use call/apply to pass Orange's this to the method.
                _orangeClosureMethod.call(this, 'via call()');
                // Calling without call/apply and "this" refers to the function's owner,
                // which is the window since this is within a window-level (global) closure.
                // That is, it's not our Orange's "this", which could lead to unexpected behavior!
                // Note that: "this._orangeClosureMethod()" does not exist.
                _orangeClosureMethod('direct invocation (note that "this" is the window)');
            },
            getName: function() {
                return 'Orange';
            },
            toString: function() {
                return this.getName();
            }
        };

        // The alternate way of declaring methods using prototype
        FruitNamespace.Orange.prototype.getOrangeZest = function() {
            console.log('getOrangeZest() ' + this.getName());
        };

    })(); // end of Orange closure



    //////////////////////////////////
    // Class inheritance using prototype. (Classical inheritance.)
    //
    (function() {
        FruitNamespace.Apple = function() {
            this.appleName = 'apple';
            this.baseData = 'apple\'s base data';
            console.log('Apple ctor.');
        };
        FruitNamespace.Apple.prototype = {
            getName: function() {
                return this.appleName;
            },
            getLabel: function() {
                return 'apple label';
            },
            getBaseData: function() {
                return this.baseData;
            },
            toString: function() {
                return this.getName();
            }
        };

        // Declare that FujiApple is an (inherits from) Apple.
        // "FujiApple.prototype = new FruitNamespace.Apple()" assigns the prototype to Apple's constructor function.
        // This has the disadvantage of invoking the Apple constructor
        // at the time the prototype is declared below.
        //
        // The base Apple ctor is NOT invoked again
        // when we do "new FujiApple()" unless we
        // explicitly call Apple.call(this) as shown.
        //
        // If the Apple ctor takes time/resources, there are other ways of performing inheritance that are less clear
        // but avoid the invocation-on-declaration problem. (See JQuery extend() implementation.)
        FruitNamespace.FujiApple = function() {
            // Call base class constructor.
            FruitNamespace.Apple.call(this);

            // Overwrite Apple's appleName with our derived class's name.
            this.appleName = 'fuji apple (getName has the derived class name)';
            console.log('FujiApple ctor.');
        };
        FruitNamespace.FujiApple.prototype = new FruitNamespace.Apple();
        FruitNamespace.FujiApple.prototype.parent = FruitNamespace.Apple.prototype;
        // Ensure that our derived class constructor is called when we do "new FujiApple()".
        FruitNamespace.FujiApple.constructor = FruitNamespace.FujiApple

        // Override Apple's getLabel().
        // Note that we cannot use
        // "FruitNamespace.FujiApple.prototype = { getName: ... }"
        // or we would lose the inheritance.
        FruitNamespace.FujiApple.prototype.getLabel = function() {
            return 'fuji apple label (getLabel was overridden)';
        };
        FruitNamespace.FujiApple.prototype.getLabelFromBase = function() {
            // Call the base class's getLabel
            return 'FujiApple.getLabelFromBase() Got the label via Apple base: '
                    + FruitNamespace.Apple.prototype.getLabel.call(this);
        };
        FruitNamespace.FujiApple.prototype.getLabelFromBaseViaParent = function() {
            // Call the base class's getLabel
            return 'FujiApple.getLabelFromBase() Got the label via Apple base via parent: '
                    + this.parent.getLabel.call(this);
        };
    })();

    //////////////////////////////////
    // Class definition using closures (functions).
    //
    // We don't need an additional anonymous closure here as we did for Orange: "(function() { })();"
    // since everything is contained within the ctor function.
    FruitNamespace.Pear = function(color) {
        // "this" is the new Pear, but only at the time the constructor is called.
        console.log('Pear ctor called. this: ' + this);
        // Alias that = this so that functions declared below can access the
        // object instance's this, rather than the caller's this.
        var that = this;

        // An instance variable. Each Pear has its own copy due to the closure scope.
        var _color = color;

        // Private method.
        var _pearClosureMethod = function(message) {
            // "this" will be wrong if call()/apply() is not used.
            console.log('_pearClosureMethod() called with arg: ' + message
                    + '  this: ' + this  + '  that: ' + that
                    + '  that.getName: ' + that.getName());
        };
        // Public methods/members are declared on the returned object.
        // This is executed every time that "new Pear()" is called,
        // and causes all Pears to have a copy of these functions. (Waste of memory.)
        this.removePeel = function() {
            // this is the Pear, so we can call this.getName()
            console.log('removePeel() Removing Pear peel: ' + that.getName() + '   color: ' + _color);

            // Call with call()/apply() and this Pear's "this".
            _pearClosureMethod.apply(that, ['via apply()']);
            // Calling the method without apply and "this" will still refer to the window.
            _pearClosureMethod('direct invocation (note that "this" is the window)');
        };
        this.getName = function() {
            return 'Pear';
        };
        this.toString = function() {
            return this.getName();
        };
    };

    //////////////////////////////////
    // Class inheritance using functions.
    //
    FruitNamespace.AsianPear = function(color) {
        var that = this;
        // Call the base class constructor.
        FruitNamespace.Pear.call(this, color);

        // New method only in derived class.
        this.showAsianPearInfo = function() {
            console.log('AsianPear showAsignPearInfo(): Asian pears are yummy.');
        };

        // Override base class method.
        var _baseRemovePeel = this.removePeel;
        this.removePeel = function() {
            console.log('AsianPear removePeel() invoking parent:');
            _baseRemovePeel();
        };
    };


    //////////////////////////////////
    // Class inheritance using prototype objects (not .prototype). (Prototypal inheritance)
    // (As shown in book: Pro JavaScript Design Patterns.)

    FruitNamespace.clone = function(obj) {
        var f = function() { };
        f.prototype = obj;
        return new f();
    };

    FruitNamespace.Gourd = {
        name: 'gourd',
        getName: function() {
            return this.name;
        },
        getBaseInfo: function() {
            return 'Gourd getBaseInfo()';
        },
        toString: function() {
            return this.name;
        }
    };
    FruitNamespace.Cucumber = FruitNamespace.clone(FruitNamespace.Gourd);
    FruitNamespace.Cucumber.name = 'cucumber';
})(window);

//////////////////////////////////
// Tests
//
(function(window) {
    window.RunExample = function() {
        console.log('__________ Testing Oranges:   Prototype classes.');
        var orange = new FruitNamespace.Orange();
        orange.removePeel();
        orange.getOrangeZest();
        // With classes defined by prototype,
        // we cannot call instance methods directly using function alias variables.
        // "this" in the Orange's prototype methods will refer to the window, not to the orange instance.
        var orangeRemovePeel = orange.removePeel;
        try {
            console.log('Invoking orange.removePeel() via a function alias:  (expecting failure)');
            orangeRemovePeel();
        }
        catch(ex) {
            console.log('As expected, failed to invoke orange.removePeel() via a function alias: ' + ex);
        }
        console.log('Invoking orange.removePeel() via a function alias using call(orange):');
        //
        // We can, however, invoke orange.removePeel() via the alias by explicitly specifying the instance.
        //
        orangeRemovePeel.call(orange);


        console.log('__________ Testing Apples:   Classical Inheritance using prototype');
        // Demonstrate inheritance.
        var appleInvoker = function(apple) {
            console.log('apple is: ' + apple);
            console.log('getLabel(): ' + apple.getLabel());
            console.log('getBaseData(): ' + apple.getBaseData());
            if(typeof apple.getLabelFromBase == typeof Function) {
                console.log(apple.getLabelFromBase());
            }
        }
        var apple = new FruitNamespace.Apple();
        var fujiApple = new FruitNamespace.FujiApple();
        appleInvoker(apple);
        appleInvoker(fujiApple);

        console.log('Updated Apple\'s base data. FujiApple\'s Apple base data unaffected.');
        apple.baseData = 'Mutated Apple base data.';
        appleInvoker(apple);
        appleInvoker(fujiApple);

        try {
            console.log('Invoking apple.getName() via a function alias.');
            var appleGetName = apple.getName;
            console.log('apple.getName() via alias: ' + appleGetName()
                + '   (Expected undefined because "this" was the window, not the apple instance!)');
        }
        catch(exApple) {
            console.log('Failed to invoke apple.getName() via a function alias:' + exApple);
        }
        

        console.log('__________ Testing Pears:    Closure classes.');
        var pearGreen = new FruitNamespace.Pear('green');
        var pearWhite = new FruitNamespace.Pear('white');
        var asignPear = new FruitNamespace.AsianPear('offwhite');
        pearGreen.removePeel();
        pearWhite.removePeel();
        asignPear.removePeel();
        asignPear.showAsianPearInfo();
        var pearRemovePeel = pearGreen.removePeel;
        // With classes defined by closures (functions), we have used "var that = this" in the
        // class definition, so we can alias its functions and "that" will still refer to the object instance's "this".
        try {
            console.log('Invoking pearGreen.removePeel() via a function alias (expect success):');
            pearRemovePeel();
        }
        catch(ex) {
            console.log('Failed to invoke pearGreen.removePeel() via a function alias: ' + ex);
        }



        console.log('__________ Testing simple classes:');
        // Simplified example of creating a "class" using only the constructor.
        (function() {
        var tmpNamespace = {};
        tmpNamespace.CtorBasedObject = function(data) {
            var that = this;
            // "this" is the new CtorBasedObject object instance.
            this.callMe = function() {
                console.log('CtorBasedObject callMe(): data: ' + this.data + '   this: ' + this  + '  that: ' + that);
            };
            this.data = data;
            this.toString = function() {
                return 'CtorBasedObject: ' + this.data;
            }
        };
        var obj1 = new tmpNamespace.CtorBasedObject('obj1');
        var obj2 = new tmpNamespace.CtorBasedObject('obj2');
        obj1.callMe();
        obj2.callMe();

        })();

        console.log('__________ Testing prototype object (prototypal) inheritance:');
        var gourd = FruitNamespace.clone(FruitNamespace.Gourd);
        var cucumber = FruitNamespace.clone(FruitNamespace.Cucumber);
        var gourdInvoker = function(gourd) {
            console.log('gourd is: ' + gourd);
            console.log('getName(): ' + gourd.getName());
            console.log('getBaseInfo(): ' + gourd.getBaseInfo());
        }
        gourdInvoker(gourd);
        gourdInvoker(cucumber);

    };
})(window);
