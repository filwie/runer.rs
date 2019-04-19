use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    for arg in args {
        let stripped = arg.replace(|c: char| !c.is_ascii_alphanumeric(), "");
        println!("{}", stripped);
    }
}
