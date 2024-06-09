use floem::cosmic_text::{Attrs, AttrsList, Stretch, Style, Weight};
use floem::keyboard::Modifiers;
use floem::peniko::Color;
use floem::reactive::{create_effect, RwSignal};
use floem::views::button;
use floem::views::editor::id::EditorId;
use floem::views::editor::layout::TextLayoutLine;
use floem::views::editor::text::{default_dark_color, SimpleStylingBuilder, Styling};
use floem::views::editor::EditorStyle;
use floem::{
    cosmic_text::FamilyOwned,
    keyboard::{Key, NamedKey},
    views::{
        editor::{
            core::{editor::EditType, selection::Selection},
            text::WrapMethod,
        },
        stack, text_editor, Decorators,
    },
};
use floem::{IntoView, View};
use std::borrow::Cow;
use std::rc::Rc;
use core::ops::Range;
use std::fs::File;
use std::io::Read;
use std::io;

fn read_file_content(file_path: &str) -> io::Result<String> {
    // Open the file
    let mut file = File::open(file_path)?;
    
    // Create a string to hold the file contents
    let mut contents = String::new();
    
    // Read the file into the string
    file.read_to_string(&mut contents)?;
    
    // Return the file contents
    Ok(contents)
}

struct EditorStyling {
    font_size: RwSignal<usize>,
    pub style: Rc<dyn Styling>,
}

impl Styling for EditorStyling {
    fn id(&self) -> u64 {
        0
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

        // todo this can be improved
        if line == 0 {
            let mut attr = Attrs::new().color(Color::WHITE);
            attr.font_size = 20 as f32;
            attrs.add_span(Range { start: 0, end: 10 }, attr);
        }else if line == 2{
            let mut attr = Attrs::new().color(Color::WHITE).weight(Weight::BOLD);
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
        self.style
            .apply_layout_styles(edid, style, line, layout_line)
    }

    fn paint_caret(&self, edid: EditorId, line: usize) -> bool {
        self.style.paint_caret(edid, line)
    }
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

    let font_size = RwSignal::new(14_usize);
    let style = EditorStyling { style: Rc::new(global_style), font_size: font_size.clone() };

    let file_content =  "Big text! Now normal text!\nNothing special in this line\nBut now bold! normal again
    ";
    let mut editor = text_editor(
        file_content
    );

    let hide_gutter = RwSignal::new(false);

    editor = editor
        .styling(style)
        .editor_style(default_dark_color)
        .editor_style(move |s| s.hide_gutter(hide_gutter.get()))
        .style(|s| s.size_full().padding(20.0));

    let doc = editor.doc();

    // Signal to hold the document content
    let doc_content = RwSignal::new(String::new());

    let view = stack((
        editor,
        stack((
            button(|| "Clear").on_click_stop(move |_| {
                doc.edit_single(
                    Selection::region(0, doc.text().len()),
                    "",
                    EditType::DeleteSelection,
                );
            }),
            button(|| "Gutter").on_click_stop(move |_| {
                hide_gutter.update(|hide| *hide = !*hide);
            }),
        ))
        .style(|s| s.width_full().flex_row().items_center().justify_center()),
    ))
    .style(|s| s.size_full().flex_col().items_center().justify_center());

    let id = view.id();
    view.on_key_up(Key::Named(NamedKey::F11), Modifiers::empty(), move |_| {
        id.inspect()
    })
}

fn main() {
    floem::launch(app_view)
}