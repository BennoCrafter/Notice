use core::ops::Range;
use floem::cosmic_text::{Attrs, AttrsList, Stretch, Style, Weight};
use floem::keyboard::Modifiers;
use floem::peniko::Color;
use floem::views::editor::id::EditorId;
use floem::views::editor::layout::TextLayoutLine;
use floem::views::editor::text::{default_dark_color, SimpleStylingBuilder, Styling};
use floem::views::editor::EditorStyle;
use floem::{
    cosmic_text::FamilyOwned,
    keyboard::{Key, NamedKey},
    views::{editor::text::WrapMethod, stack, text_editor, Decorators},
};
use floem::{IntoView, View};
use std::fs::File;
use std::io;
use std::io::Read;
use std::rc::Rc;
use lazy_static::lazy_static;
use std::sync::{Mutex, Arc};

/* fn read_file_content(file_path: &str) -> io::Result<String> {
    // Open the file
    let mut file = File::open(file_path)?;

    // Create a string to hold the file contents
    let mut contents = String::new();

    // Read the file into the string
    file.read_to_string(&mut contents)?;

    // Return the file contents
    Ok(contents)
} */

lazy_static! {
    static ref CURRENT_CURSOR_LINE: Arc<Mutex<usize>> = Arc::new(Mutex::new(0));
}

struct EditorStyling {
    pub style: Rc<dyn Styling>,
}

impl Styling for EditorStyling {
    fn id(&self) -> u64 {
        self.style.id()
    }

    fn apply_attr_styles(
        &self,
        _edid: EditorId,
        _style: &EditorStyle,
        line: usize,
        _default: Attrs, 
        attrs: &mut AttrsList,
    ) {
        attrs.clear_spans();
        println!("executed style on line: {}", line);
        if line == 0 {
            let attr = Attrs::new().color(Color::WHITE).font_size(20.0);
            attrs.add_span(Range { start: 0, end: 10 }, attr);
        } else if line == 2 {
            let attr = Attrs::new().color(Color::WHITE).weight(Weight::BOLD);
            attrs.add_span(Range { start: 0, end: 14 }, attr);
        }
    }

    fn apply_layout_styles(
        &self,
        edid: EditorId,
        style: &EditorStyle,
        line: usize,
        layout_line: &mut TextLayoutLine,
    ) {
        self.style.apply_layout_styles(edid, style, line, layout_line)
    }

    fn paint_caret(&self, edid: EditorId, line: usize) -> bool {
        // println!("Current cursor line: {}", line);
        *CURRENT_CURSOR_LINE.lock().unwrap() = line;
        self.style.paint_caret(edid, line)
    }
    
    fn font_size(&self, _edid: EditorId, _line: usize) -> usize {
        16
    }
    
    fn line_height(&self, edid: EditorId, line: usize) -> f32 {
        let font_size = self.font_size(edid, line) as f32;
        (1.5 * font_size).round().max(font_size)
    }
    
    fn font_family(&self, _edid: EditorId, _line: usize) -> std::borrow::Cow<[FamilyOwned]> {
        std::borrow::Cow::Borrowed(&[FamilyOwned::SansSerif])
    }
    
    fn weight(&self, _edid: EditorId, _line: usize) -> Weight {
        Weight::NORMAL
    }
    
    fn italic_style(&self, _edid: EditorId, _line: usize) -> floem::cosmic_text::Style {
        floem::cosmic_text::Style::Normal
    }
    
    fn stretch(&self, _edid: EditorId, _line: usize) -> Stretch {
        Stretch::Normal
    }
    
    fn indent_line(&self, _edid: EditorId, line: usize, _line_content: &str) -> usize {
        line
    }
    
    fn tab_width(&self, _edid: EditorId, _line: usize) -> usize {
        4
    }
    
    fn atomic_soft_tabs(&self, _edid: EditorId, _line: usize) -> bool {
        false
    }
}

lazy_static! {
    static ref SKIP_INIT_ATTRS_LOAD: Mutex<bool> = Mutex::new(true);
}

fn toggle_skip_init_attrs_load(new_value: bool) {
    let mut skip_init = SKIP_INIT_ATTRS_LOAD.lock().unwrap();
    *skip_init = new_value;
}

fn app_view() -> impl IntoView {

    let global_style = SimpleStylingBuilder::default()
        .wrap(WrapMethod::None)
        .font_family(vec![
            FamilyOwned::Name("Fira Code".to_string()),
            FamilyOwned::Name("Consolas".to_string()),
            FamilyOwned::Monospace,
        ])
        .build();

    let style = EditorStyling {
        style: Rc::new(global_style),
    };
    let file_content =
        "Big text! Now normal text!\nNothing special in this line\nBut now bold! normal again";

    let editor = text_editor(file_content);

    let editor = editor
        .styling(style)
        .editor_style(default_dark_color)
        .editor_style(move |s| s.hide_gutter(true))
        .style(|s| s.size_full().padding(20.0))
        .update(move |update| {
            if let Some(editor) = &update.editor {
                println!("Update: {}", editor.doc().text());
            } else {
                println!("No editor available to provide an update.");
            }
        });

    let doc = editor.doc();
    let view = stack((editor,)).style(|s| s.size_full().flex_col().items_center().justify_center());
    let id = view.id();
    view.on_key_up(Key::Named(NamedKey::F11), Modifiers::empty(), move |_| {
        id.inspect()
    })

}

fn main() {
    floem::launch(app_view);
}