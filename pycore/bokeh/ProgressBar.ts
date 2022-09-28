import {Markup, MarkupView} from "models/widgets/markup"
import * as p from "core/properties"

export class ProgressBarView extends MarkupView {
  override model: ProgressBar

  override render(): void {
    super.render()

    this.markup_el.innerHTML = `


<style>

.progress {
  margin:0px auto;
  padding:0;
  width:${this.model.width!}px;
  height:${this.model.height!}px;
  overflow:hidden;
  background:#e5e5e5;
  border-radius:6px;
}

.bar {
  position:relative;
  float:left;
  min-width:1%;
  height:100%;
  background:${this.model.color};
}

.percent {
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  margin:0;
}

</style>

  <div class="progress">
    <div class="bar" style="width:${this.model.progress}%">
    </div>
    <p class="percent">${this.model.text}</p>
  </div>


`

  }
}

export namespace ProgressBar {
  export type Attrs = p.AttrsOf<Props>

  export type Props = Markup.Props & {
    render_as_text: p.Property<boolean>
    progress: p.Property<number>
    color: p.Property<string>
  }
}

export interface ProgressBar extends ProgressBar.Attrs {}

export class ProgressBar extends Markup {
  override properties: ProgressBar.Props
  override __view_type__: ProgressBarView

  constructor(attrs?: Partial<ProgressBar.Attrs>) {
    super(attrs)
  }

  static {
    this.prototype.default_view = ProgressBarView

    this.define<ProgressBar.Props>(({Boolean, Number, String}) => ({
      render_as_text: [ Boolean, false ],
      progress: [Number, 10],
      color: [String, "cornflowerblue"]
    }))
  }
}