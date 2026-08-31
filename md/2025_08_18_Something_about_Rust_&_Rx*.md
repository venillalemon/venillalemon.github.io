# Something about Rust & Rx*

*August 18, 2025*

## Names of associated items

类方法、类中 associated const item 都属于 value namespace. 但是由于一个 `struct` 可以有多个 `impl` 块，仍然会有重名发生.

```rust
enum D {
    A,
    B,
    C,
}

impl Int for D {
    const FN: i32 = 1926;
    fn get(&self) -> i32 {
        match self {
            D::A => 1,
            D::B => 2,
            D::C => 3,
        }
    }
}

impl Str for D {
    fn get(&self) -> String {
        match self {
            D::A => String::from("A"),
            D::B => String::from("B"),
            D::C => String::from("C"),
        }
    }
}

impl D {
    fn get(&self) -> i32 {
        114514
    }
}

impl Con for D {}

struct P {}

impl Int for P {
    const FN: i32 = 2026;
    fn get(&self) -> i32 {
        1919810
    }
}

trait Int {
    const FN: i32;
    fn get(&self) -> i32;
}

trait Str {
    fn get(&self) -> String;
}

trait Con {
    const FN: i32 = 0817;
}
struct Y {
    i: i32,
    p: i32,
}

fn g(d: i32, ff: &str) -> [i32; 2] {
    let mut a = [0; 2];
    a[0] = d;
    a[1] = ff.len() as i32;
    a
}
fn main() {
    let d = D::B;
    println!("{}", D::get(&d)); // 114514
    println!("{}", Int::get(&d)); // 2
    let p = P {};
    println!("{}", Int::get(&p)); // 1919810
    println!("{}", Str::get(&d)); // B
    println!("{}", d.get()); // 114514
    println!("{}", P::FN); // 2026
    // println!("{}", D::FN); // error
    // println!("{}", Int::FN); // error
    // println!("{}", Con::FN); // error
    println!("{}", <D as Con>::FN); // 817
    println!("{}", <D as Int>::FN); // 1926
    println!(
        "{:?}",
        g({ 123 }, "Hello") // [123, 5]
    );
}
```

总之 1.field 和 method 可以重名；2.默认用 inherent impl 的 associated item, 它会覆盖 trait impl 的同名 item；3.如果要用 trait impl 的同名 item, 需要显式指定 trait 名.

有时候 method 中没有 `&self` 参数，这样就必须用 `as` 指定调用的是哪个 `struct` 的 method.

## Nested `impl`

```rust
struct G {}

trait Get {
    fn get(&self) -> i32 {
        19260817
    }
}
fn max(x: i32, y: i32) -> i32 {
    struct G {
        a: i32,
    }
    impl crate::G { // 1
        fn get() -> G {
            G { a: 1919810 }
        }
    }
    if x > y {
        impl Get for G {} // 2
        return x;
    }
    y
}
fn main() {
    let g = G::get();
    println!("{}", g.get()); // 19260817
}
```

情况 1，编译器直接按照路径寻找，得到的是函数外的空结构体；情况 2，在当前 scope 中寻找 `G`, 没找到继续回溯，直到在函数体这一层找到.

同时，`g` 的类型是通过类型推导得到的，编译器会在 `G::get()` 处推导出 `G` 的类型，并且知道这个 `G` 不仅仅有一个 field，还有个 `get` 方法. (用 `Ctrl` 是点不开这个 `g.get()` 的)

## Copy, Clone and Reference

区分 `Copy` 和 `move` 语义的目的在于，浅拷贝容易出现 double free 的问题，例如带有堆上数据的数据结构 `String` `Box<T>`. 这一点，lifetime 和 `Drop` 机制是联合作用的，变量离开作用域时，`Drop` 会被调用，释放堆上数据. `Copy` trait 只有当数据结构中所有 field 都是 `Copy` 的时候，才能被自动实现.

如同标题所说，我们需要处理编译器赋值（包括传参、数组构造——其实也相当于函数传参）时编译器的细节，不能口口声声说我们删除了 `trait` 就弃之不顾。

几乎所有语言的基础类型（包括指针）都是值拷贝；对于用户自定义类型，C++ 允许用户自定义拷贝构造函数，Rust 则是通过 `Copy` trait 来标记类型是否可以值拷贝. Java 和 Python 则是引用传递. 浅拷贝可不能和引用混淆了(x).

### How does IR pass by value?

如果有一个大结构体，我们需要用传值的方式调用函数. 该怎么实现？

先考虑如何返回一个结构体. 最先想到的是存在栈上，但是肯定不可放在 Callee 的栈帧，因为调用完就没法用了. 所以需要一个指针指向 Caller 栈的某一块，这一块必须提早被 Caller 分配好.

然后就是传参，很简单直接去 Caller 栈上取就行了.

```rust
#![no_std]
#[repr(C)]
struct A {
    a: i32,
    b: [i8; 32],
}
impl A{
    #[no_mangle]
    fn add(a: Self) -> Self {
        A{a: a.a + 1, b: a.b}
    }
}
#[no_mangle]
fn main() -> () {
    let c = A::add(A{a: 4, b: [2; 32]});
    let b = c;
    printlnInt(b.a);
}
#[no_mangle]
fn printlnInt(i:i32) -> () {
    // omitted
}
```

这段代码直接复制进 [godbolt](https://godbolt.org/)，选择 Rust nightly 版本, 编译参数为：

```
--emit=llvm-ir --target=riscv64gc-unknown-none-elf -C target-cpu=generic-rv64 -C debuginfo=0
```

你也可以使用 `--target=riscv64gc-unknown-linux-gnu`, 区别是有标准库 `std`.

下面抄写部分 llvm IR 代码

```llvm
define void @main() unnamed_addr #1 {
  %_3 = alloca [32 x i8], align 1                                                       ; temporary array
  %_2 = alloca [36 x i8], align 4                                                       ; struct A
  %c = alloca [36 x i8], align 4                                                        ; for return value
  call void @llvm.memset.p0.i64(ptr align 1 %_3, i8 2, i64 32, i1 false)                ; fill array with 2
  store i32 4, ptr %_2, align 4                                                         ; set field a
  %0 = getelementptr inbounds i8, ptr %_2, i64 4                                        ; pointer to field b
  call void @llvm.memcpy.p0.p0.i64(ptr align 4 %0, ptr align 1 %_3, i64 32, i1 false)   ; copy array to field b
  call void @add(ptr sret([36 x i8]) align 4 %c, ptr align 4 %_2)                       ; call A::add, with sret the first argument
  %_5 = load i32, ptr %c, align 4                                                       ; load return value field a, note the %c ptr is used
  call void @printlnInt(i32 signext %_5)
  ret void
}
define void @add(ptr sret([36 x i8]) align 4 %_0, ptr align 4 %a) unnamed_addr #1 {
  %_5 = alloca [32 x i8], align 1
  %_3 = load i32, ptr %a, align 4
  %0 = call { i32, i1 } @llvm.sadd.with.overflow.i32(i32 %_3, i32 1)                    ; check overflow call
  %_4.0 = extractvalue { i32, i1 } %0, 0
  %_4.1 = extractvalue { i32, i1 } %0, 1                                                ; something like Result<T,E>
  br i1 %_4.1, label %panic, label %bb1

bb1:                                              ; preds = %start
  %1 = getelementptr inbounds i8, ptr %a, i64 4
  call void @llvm.memcpy.p0.p0.i64(ptr align 1 %_5, ptr align 4 %1, i64 32, i1 false)   ; copy field b to temporary array
  store i32 %_4.0, ptr %_0, align 4                                                     ; store the result a
  %2 = getelementptr inbounds i8, ptr %_0, i64 4
  call void @llvm.memcpy.p0.p0.i64(ptr align 4 %2, ptr align 1 %_5, i64 32, i1 false)   ; store field b
  ret void                                                                              ; return void

panic:                                            ; preds = %start
  call void @_ZN4core9panicking11panic_const24panic_const_add_overflow17h446c73c159762aceE(ptr align 8 @alloc_7c1e053569136b9ce98c807d1b3e2690) #6
  unreachable
}
```

关于为什么用 `memcpy` 来初始化 array，你可以尝试把 `i8` 改成 `i32`, 它就会手写循环来赋值. 后面各种移动当然还是 `memcpy`; 至于我们的 `RCompiler`, 我想循环就够了.

## Const

```rust
fn main() {
    let f: &mut i32 = &mut X;
    *f = 4;
    println!("{}", X); // 5
    let f = &mut F;
    *f = A { x: 3, y: 4 };
    println!("F.x: {}, F.y: {}", F.x, F.y); // 1, 2
    println!("f.x: {}, f.y: {}", f.x, f.y); // 3, 4
}

const X: i32 = 5;

struct A {
    x: i32,
    y: i32,
}

const F: A = A { x: 1, y: 2 };
```

> Constants are essentially inlined wherever they are used, meaning that they are **copied directly into the relevant context when used**. This includes usage of constants from external crates, and non-Copy types. References to the same constant are not necessarily guaranteed to refer to the same memory address.

就像其他的 literal 一样，const 也完全支持 `&mut`, 不过你只能通过 `&mut` 修改它的某个副本.

## Autoref and Autoderef

主要讨论 method call 中的自动引用和解引用. 我们针对没有实现 `Copy` trait 的 `struct A` 来分类讨论：

- 如果最外层引用非 mutable，不能转为任何最外层是 `mut` 的引用

- 最外层 `&mut` 可以转为 `&`，内层不行

- 在此基础上，可以任意增加不可变借用 `&`, 可以任意解引用 `*` (意味着可以任意去掉 `&mut` 或 `&`)

- 涉及到所有权移动，例如传值的情况，只有类型 `A` 的变量可以作为参数传入，其他都不行; 因为不能说某个表达式 (例如 `**a`) 持有该数据的所有权.

可以自己验证，不保证完全正确，但是覆盖了绝大多数情况.
