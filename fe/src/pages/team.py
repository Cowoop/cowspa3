import sphc
import fe.bases

tf = sphc.TagFactory()
BasePage = fe.bases.CSAuthedPage

def get_team_form():
    form = sphc.more.Form(id='team_form', classes=['hform', 'simple-hform'])

    form.add_field('Name', tf.INPUT(type='text', id='member_name',
        name='member_name'))
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
        team_tmpl.box.label = tf.LABEL("${user}", Class='team-title')
        team_tmpl.box.link = tf.A("X", id='delete_link-${user_id}', href='',
                Class='remove_staff')

        teams.team_tmpl = team_tmpl

        container.teams = teams

        #                                   New Team Member
        form = get_team_form()
        form.add_buttons(tf.BUTTON("Add", id='save-btn', type="submit"))
        container.form = form.build()

        container.script = sphc.more.script_fromfile("fe/src/js/team.js")
        return container
