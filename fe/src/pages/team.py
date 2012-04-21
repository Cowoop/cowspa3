import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def get_team_form():
    form = sphc.more.Form(id='team_form', classes=['hform'])

    form.add_field('Name', tf.INPUT(type='text', id='member_name', name='member_name'))
    roles = tf.DIV(fe.src.common.team_options, id='roles')
    form.add_field('Role', roles)

    return form

class List(BasePage):
    current_nav = 'Team'
    title = 'Team'

    def content(self):
        container = tf.DIV()

        new_team_member = tf.BUTTON("New Team Member", id="new-team", type='button')
        container.button = new_team_member

        teams = tf.DIV(id="team_list")
        team_tmpl = sphc.more.jq_tmpl('team_tmpl')
        team_tmpl.box = tf.DIV(Class='team-box')
        team_tmpl.box.name = tf.DIV(Class='team_name_part')
        team_tmpl.box.name.label = tf.LABEL("${name}", Class='team-title')
        team_tmpl.box.roles = tf.DIV(Class='team_roles_part', id='roles-${id}')
        team_tmpl.box.roles.chkboxes = tf.DIV(fe.src.common.team_options, id='chkboxes-${id}')
        team_tmpl.box.roles.stat = tf.LABEL(" ", Class='action-status')
        team_tmpl.box.btns = tf.DIV(Class='team_delete_btn_part')
        team_tmpl.box.btns.upd = tf.BUTTON("Update", id='upd_team-${id}', type='button', Class='update_staff')
        team_tmpl.box.btns.remove = tf.A("X", id='delete_link-${id}', href='#', Class='remove_staff')

        container.team_tmpl = team_tmpl

        container.teams = teams

        # New Team Member
        form = get_team_form()
        form.add_buttons(tf.BUTTON("Add", id='save-btn', type="submit"))
        container.form = form.build()

        container.script = sphc.more.script_fromfile("fe/src/js/team.js")
        return container
