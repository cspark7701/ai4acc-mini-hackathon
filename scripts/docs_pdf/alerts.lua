-- Render GitHub alert blockquotes (> [!NOTE], > [!TIP], ...) as styled boxes.
function BlockQuote(el)
  local first = el.content[1]
  if not first or (first.t ~= "Para" and first.t ~= "Plain") then return nil end
  local txt = pandoc.utils.stringify(first.content[1] or "")
  local kind = txt:match("^%[!(%u+)%]$")
  if not kind then return nil end
  table.remove(first.content, 1)
  while first.content[1] and (first.content[1].t == "SoftBreak" or first.content[1].t == "LineBreak" or first.content[1].t == "Space") do
    table.remove(first.content, 1)
  end
  local label = kind:sub(1,1) .. kind:sub(2):lower()
  local title = pandoc.Div({pandoc.Plain({pandoc.Strong({pandoc.Str(label)})})}, {class = "alert-title"})
  table.insert(el.content, 1, title)
  return pandoc.Div(el.content, {class = "alert alert-" .. kind:lower()})
end
